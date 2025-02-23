from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout    
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.widget import MDWidget
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from main import process_prompt
from OCR import add_timetable_to_db
import speech_recognition as sr

try:
    from plyer import filechooser
except ImportError as e:
    print(f"Error importing plyer: {e}")
import os
import json
import traceback

# KV String with Material Design components
Builder.load_string('''
#:kivy 2.0
#:import md_colors kivymd.color_definitions.colors

<ChatMessage>:
    adaptive_height: True
    padding: dp(10)
    size_hint_y: None
    height: message_label.height + dp(20)
    md_bg_color: app.theme_cls.primary_light if root.is_user else app.theme_cls.bg_darkest
    radius: [15,]   
    
    MDLabel:
        id: message_label
        text: root.message
        theme_text_color: "Custom"
        text_color: app.theme_cls.text_color
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width - dp(20), None
        halign: 'left'
        valign: 'top'
        padding_x: dp(10)
        padding_y: dp(5)

<WelcomeScreen>:
    name: 'welcome'
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(30)
        md_bg_color: app.theme_cls.bg_normal
        
        MDLabel:
            text: 'Welcome to AI Chat Assistant'
            font_style: 'H3'
            bold: True
            size_hint_y: None
            height: dp(100)
            halign: 'center'
            theme_text_color: "Primary"
            
        Image:
            source: 'microphone_new.png'  # Replace with your app logo
            size_hint: None, None
            size: dp(200), dp(200)
            pos_hint: {'center_x': 0.5}
            
        MDLabel:
            text: 'Your intelligent chat assistant for document analysis and conversation'
            font_style: 'Body1'
            size_hint_y: None
            height: dp(80)
            halign: 'center'
            theme_text_color: "Secondary"
            
        MDRaisedButton:
            text: 'Start Chatting'
            size_hint: None, None
            height: dp(60)
            width: dp(200)
            pos_hint: {'center_x': 0.5}
            md_bg_color: app.theme_cls.primary_color
            font_size: '20sp'
            on_release: root.manager.transition.direction = 'left'; root.manager.current = 'chat'
            
        MDRaisedButton:
            text: 'Settings'
            size_hint: None, None
            height: dp(60)
            width: dp(200)
            pos_hint: {'center_x': 0.5}
            md_bg_color: app.theme_cls.accent_color
            font_size: '20sp'
            on_release: root.manager.transition.direction = 'left'; root.manager.current = 'settings'

<SettingsScreen>:
    name: 'settings'
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(20)
        md_bg_color: app.theme_cls.bg_normal
        
        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            
            MDIconButton:
                icon: "arrow-left"
                on_release: root.manager.transition.direction = 'right'; root.manager.current = 'welcome'
                theme_text_color: "Primary"
                
            MDLabel:
                text: 'Settings'
                font_style: 'H5'
                bold: True
                theme_text_color: "Primary"
                
        MDScrollView:
            do_scroll_x: False
            bar_width: dp(4)
            bar_color: app.theme_cls.primary_color
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(30)
                padding: dp(20)
                adaptive_height: True
                
                # Theme Settings
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(200)
                    padding: dp(16)
                    spacing: dp(10)
                    md_bg_color: app.theme_cls.bg_light
                    radius: [10,]
                    
                    MDLabel:
                        text: 'Theme'
                        font_style: 'H6'
                        size_hint_y: None
                        height: dp(30)
                        theme_text_color: "Primary"
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(10)
                        
                        MDBoxLayout:
                            spacing: dp(15)
                            adaptive_height: True
                            size_hint_x: 0.98
                            MDLabel:
                                text: 'Dark Mode'
                                theme_text_color: "Secondary"
                                size_hint_x: 0.5
                                
                            MDSwitch:
                                id: theme_switch
                                size_hint_x: None
                                width: dp(35)
                                
                                active: app.theme_cls.theme_style == "Dark"
                                on_active: app.switch_theme(self.active)
                                
                        
                        MDBoxLayout:
                            spacing: dp(15)
                            adaptive_height: True
                            
                            MDLabel:
                                text: 'Primary Color'
                                theme_text_color: "Secondary"
                                size_hint_x: 0.5
                            
                            MDBoxLayout:
                                spacing: dp(5)
                                adaptive_size: True
                                
                                MDIconButton:
                                    icon: "circle"
                                    md_bg_color: [0,0,0,0]
                                    theme_text_color: "Custom"
                                    text_color: md_colors["Blue"]["A700"]
                                    on_release: app.change_primary_color("Blue")
                                    
                                MDIconButton:
                                    icon: "circle"
                                    md_bg_color: [0,0,0,0]
                                    theme_text_color: "Custom"
                                    text_color: md_colors["Red"]["A700"]
                                    on_release: app.change_primary_color("Red")
                                    
                                MDIconButton:
                                    icon: "circle"
                                    md_bg_color: [0,0,0,0]
                                    theme_text_color: "Custom"
                                    text_color: md_colors["Teal"]["A700"]
                                    on_release: app.change_primary_color("Teal")
                                    
                                MDIconButton:
                                    icon: "circle"
                                    md_bg_color: [0,0,0,0]
                                    theme_text_color: "Custom"
                                    text_color: md_colors["Purple"]["A700"]
                                    on_release: app.change_primary_color("Purple")
                
                # Voice Settings
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(160)
                    padding: dp(16)
                    spacing: dp(10)
                    md_bg_color: app.theme_cls.bg_light
                    radius: [10,]
                    
                    MDLabel:
                        text: 'Voice Settings'
                        font_style: 'H6'
                        size_hint_y: None
                        height: dp(30)
                        theme_text_color: "Primary"
                    
                    MDBoxLayout:
                        spacing: dp(15)
                        adaptive_height: True
                        size_hint_x: 0.98
                        MDLabel:
                            text: 'Enable Voice Input'
                            theme_text_color: "Secondary"
                            size_hint_x: 0.5
                            
                        MDSwitch:
                            size_hint_x: None
                            width: dp(35)
                            active: True
                            
                        
                            
                
                MDRaisedButton:
                    text: 'Reset to Default'
                    size_hint: None, None
                    size: dp(200), dp(50)
                    pos_hint: {'center_x': 0.5}
                    md_bg_color: (0.8, 0.2, 0.2, 1)

<ChatScreen>:
    name: 'chat'
    file_display: file_display
    
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)
        md_bg_color: app.theme_cls.bg_normal
        
        # Left side (Chat interface)
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: dp(20) 
            size_hint_x: 0.7
            
            # Header
            MDBoxLayout:
                size_hint_y: None
                height: dp(50)
                spacing: dp(10)
                padding: [dp(10), 0, dp(10), 0] 
                
                MDIconButton:
                    icon: "home"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    size_hint_x: None
                    width: dp(48)
                    pos_hint: {'center_y': 0.5}
                    on_release: root.manager.transition.direction = 'right'; root.manager.current = 'welcome'
                

                MDIconButton:
                    icon: "cog"  
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    size_hint_x: None
                    width: dp(48)
                    pos_hint: {'center_y': 0.5}
                    on_release: root.manager.transition.direction = 'left'; root.manager.current = 'settings'

                MDLabel:
                    text: 'AI BOT'
                    font_style: 'H4'
                    bold: True
                    halign: 'right'
                    

                MDWidget:
                    size_hint_x: 1

            # # Title
           
            #     
            #     size_hint_y: None
            #     height: dp(80)
            #    
            #     theme_text_color: "Primary"
            #     height: self.texture_size[1]
            #     halign: 'center'
            #     canvas.before:
            #         Color:
            #             rgba: 0.12, 0.12, 0.12, 1
            #         RoundedRectangle:
            #             pos: self.pos
            #             size: self.size
            #             radius: [20,]

            # Chat Area
            MDScrollView:
                id: chat_scroll
                do_scroll_x: False
                bar_width: dp(4)
                bar_color: app.theme_cls.primary_color
                
                MDBoxLayout:
                    id: chat_area
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(30)  # Increased spacing between messages
                    padding: dp(10)

            # Input area with voice button on the right
            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                spacing: dp(10)
                padding: dp(10)

                MDTextField:
                    id: message_input
                    hint_text: 'How can I help you?'
                    multiline: False
                    size_hint_x: 1
                    on_text_validate: root.send_message()
                    mode: "fill"
                    radius: [20, 20, 20, 20]
                    text_color: 1, 1, 1, 1
                    hint_text_color: 0.7, 0.7, 0.7, 1
                    

                MDIconButton:
                    id: voice_button
                    icon: "microphone"
                    size_hint_x: None
                    width: dp(60)
                    on_press: root.start_voice_animation()
                    on_release: root.send_message()
                    md_bg_color: app.theme_cls.primary_color
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]

        # Right side (File display)
        MDCard:
            orientation: 'vertical'
            size_hint_x: 0.3
            padding: dp(10)
            md_bg_color: app.theme_cls.bg_dark
            radius: [20,]

            # Header for file preview
            MDLabel:
                text: 'File Preview'
                font_style: 'H6'
                size_hint_y: None
                height: dp(40)
                theme_text_color: "Primary"
                halign: 'center'
                    

            # File content area with ScrollView
            MDBoxLayout:
                orientation: 'vertical'
                
                MDScrollView:
                    do_scroll_x: False
                    bar_width: dp(4)
                    bar_color: app.theme_cls.primary_color
                    size_hint_y: 1

                    MDBoxLayout:
                        id: file_display
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(10) 
                        
                
                # Upload file button at the bottom of the file preview
                MDRaisedButton:
                    text: 'Upload File'
                    size_hint_y: None
                    height: dp(50)
                    pos_hint: {'center_x': 0.5}
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.safe_open_file_dialog()
''')

class ChatMessage(MDCard):
    message = StringProperty('')
    is_user = BooleanProperty(False)
    
    def on_size(self, *args):
        # Ensure the message_label updates its height 
        self.ids.message_label.text_size = (self.width - dp(20), None)
        self.height = self.ids.message_label.texture_size[1] + dp(20)

class WelcomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ChatScreen(Screen):
    current_format = StringProperty('Upload File Type')
    file_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_file = None
        self.chat_initialized = False
        # self.add_message("Hello! How can I help you today?", is_user=False)
        
    def on_enter(self):
        # Initialize chat with welcome message when entering the screen
        # This ensures the welcome message doesn't appear multiple times
        if not self.chat_initialized:
            self.add_message("Hello! How can I help you today?", is_user=False)
            self.chat_initialized = True

            self.ids.message_input.text_color_normal = [1, 1, 1, 1]
            self.ids.message_input.text_color_focus = [1, 1, 1, 1]

    def safe_open_file_dialog(self, *args):
        try:
            print("Attempting to open file dialog")
            self.open_file_dialog()
        except Exception as e:
            error_msg = f"Error in file dialog: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.add_message(error_msg, is_user=False)

    def open_file_dialog(self):
        try:
            print("Opening file chooser")
            filechooser.open_file(
                on_selection=self.handle_selection,
                multiple=False
            )
        except AttributeError as e:
            error_msg = "File chooser not available. Please check if 'plyer' is installed properly."
            print(f"{error_msg}: {e}")
            self.add_message(error_msg, is_user=False)
        except Exception as e:
            error_msg = f"Error opening file dialog: {str(e)}"
            print(f"{error_msg}\n{traceback.format_exc()}")
            self.add_message(error_msg, is_user=False)

    def handle_selection(self, selection):
        try:
            print(f"Handling selection: {selection}")
            if selection:
                self.selected_file = selection[0]
                file_name = os.path.basename(self.selected_file)
                self.current_format = file_name
                self.display_file(self.selected_file)

                # Check if the file is an image based on extension
                image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
                file_ext = os.path.splitext(file_name)[1].lower()

                if file_ext in image_extensions:
                    # Call the function to process the image and store in DB
                    result_message = add_timetable_to_db(self.selected_file)
                    self.add_message(f"Processed image: {file_name}\n{result_message}", is_user=False)
                else:
                    self.add_message(f"Uploaded file: {file_name} (not an image)", is_user=False)
            else:
                print("No file selected")
        except Exception as e:
            error_msg = f"Error handling file selection: {str(e)}"
            print(f"{error_msg}\n{traceback.format_exc()}")
            self.add_message(error_msg, is_user=False)

    def display_file(self, file_path):
        try:
            print(f"Displaying file: {file_path}")
            self.file_display.clear_widgets()
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.ipynb':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        notebook = json.load(f)
                    
                    content_layout = MDBoxLayout(
                        orientation='vertical',
                        size_hint_y=None,
                        spacing=dp(10),
                        padding=dp(10),
                        adaptive_height=True
                    )
                    
                    # Notebook metadata
                    if 'metadata' in notebook:
                        metadata_text = f"Kernel: {notebook['metadata'].get('kernelspec', {}).get('display_name', 'Unknown')}"
                        metadata_label = MDLabel(
                            text=metadata_text,
                            size_hint_y=None,
                            height=dp(30),
                            theme_text_color="Custom",
                            text_color=(0.7, 0.7, 1, 1)
                        )
                        content_layout.add_widget(metadata_label)
                    
                    # Process cells
                    for cell_num, cell in enumerate(notebook['cells'], 1):
                        cell_type = cell['cell_type'].capitalize()
                        source = ''.join(cell['source'])
                        
                        # Display cell content
                        content_label = MDLabel(
                            text=f"Cell {cell_num} ({cell_type}):\n{source}",
                            size_hint_y=None,
                            height=dp(20) * (len(source.split('\n')) + 2),
                            theme_text_color="Custom",
                            text_color=(0.2, 0.8, 0.2, 1) if cell['cell_type'] == 'code' else App.get_running_app().theme_cls.text_color,
                            text_size=(Window.width * 0.25, None),
                            halign='left',
                            valign='top'
                        )
                        content_layout.add_widget(content_label)
                        
                        # Display outputs for code cells
                        if cell['cell_type'] == 'code' and 'outputs' in cell:
                            for output in cell['outputs']:
                                output_text = ""
                                if 'text' in output:
                                    output_text = ''.join(output['text'])
                                elif 'data' in output and 'text/plain' in output['data']:
                                    output_text = ''.join(output['data']['text/plain'])
                                
                                if output_text:
                                    output_label = MDLabel(
                                        text=f"Output:\n{output_text}",
                                        size_hint_y=None,
                                        height=dp(20) * (len(output_text.split('\n')) + 2),
                                        theme_text_color="Secondary",
                                        text_size=(Window.width * 0.25, None),
                                        halign='left',
                                        valign='top'
                                    )
                                    content_layout.add_widget(output_label)
                    
                    content_layout.height = sum(child.height for child in content_layout.children)
                    self.file_display.add_widget(content_layout)
                    
                except json.JSONDecodeError:
                    self.file_display.add_widget(
                        MDLabel(
                            text="Error: Invalid Jupyter notebook file format",
                            size_hint_y=None,
                            height=dp(100),
                            theme_text_color="Error"
                        )
                    )
            
            elif file_ext in ['.png', '.jpg', '.jpeg', '.gif']:
                img = Image(source=file_path, size_hint_y=None)
                img.height = dp(300)
                self.file_display.add_widget(img)
            
            elif file_ext in ['.txt', '.py', '.json', '.csv']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_label = MDLabel(
                            text=content,
                            size_hint_y=None,
                            height=max(dp(300), len(content.split('\n')) * dp(20)),
                            text_size=(Window.width * 0.25, None),
                            halign='left',
                            valign='top',
                            theme_text_color="Primary"
                        )
                        self.file_display.add_widget(text_label)
                except UnicodeDecodeError:
                    self.file_display.add_widget(
                        MDLabel(
                            text="Unable to read file: File encoding not supported",
                            size_hint_y=None,
                            height=dp(100),
                            theme_text_color="Error"
                        )
                    )
            else:
                self.file_display.add_widget(
                    MDLabel(
                        text=f"File type {file_ext} preview not supported\nFile: {os.path.basename(file_path)}\nSize: {os.path.getsize(file_path) / 1024:.1f} KB",
                        size_hint_y=None,
                        height=dp(100),
                        theme_text_color="Secondary"
                    )
                )
        except Exception as e:
            error_msg = f"Error displaying file: {str(e)}"
            print(f"{error_msg}\n{traceback.format_exc()}")
            self.file_display.add_widget(
                MDLabel(
                    text=error_msg,
                    size_hint_y=None,
                    height=dp(100),
                    theme_text_color="Error"
                )
            )

    def send_message(self, *args):
        try:
            message = self.ids.message_input.text.strip()
            print(f"User Message Entered: {message}")  # Debugging

            if message:
                self.add_message(message, is_user=True)  # Show user message
                self.ids.message_input.text = ''

                ai_response = process_prompt(message)
                print(f"AI Response Received: {ai_response}")  # Debugging

                if not ai_response:  # Handle empty response
                    ai_response = "Sorry, I couldn't process that request."

                self.add_message(str(ai_response), is_user=False)  # Display response

                Clock.schedule_once(lambda dt: setattr(self.ids.chat_scroll, 'scroll_y', 0), 0.1)
        except Exception as e:
            print(f"Error s`ending message: {str(e)}")


    def add_message(self, message, is_user):
        try:
            # Create message widget
            message_widget = ChatMessage(
                message=message,
                is_user=is_user,
                size_hint_x=0.8,
            )

            # Create a horizontal box layout for message alignment
            h_layout = MDBoxLayout(
                size_hint_y=None, orientation = 'horizontal'
                )

            # Add spacing widget on the appropriate side
            if is_user:
                h_layout.add_widget(MDWidget(size_hint_x=0.2))
                h_layout.add_widget(message_widget)
            else:
                h_layout.add_widget(message_widget)
                h_layout.add_widget(MDWidget(size_hint_x=0.2))

            # First bind the height of message_widget to update h_layout's height
            def update_height(*args):
                h_layout.height = message_widget.height
            
            message_widget.bind(height=update_height)
            
            # Trigger initial height calculation
            h_layout.height = message_widget.height

            # Add to chat area (the spacing is set in the kv string for chat_area)
            self.ids.chat_area.add_widget(h_layout)

            Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
            # Scroll to bottom
            self.scroll_to_bottom()
        except Exception as e:
            print(f"Error adding message: {str(e)}")
    def scroll_to_bottom(self, *args):
        self.ids.chat_scroll.scroll_y = 0

    # def start_voice_animation(self):
    #     """Start animation when voice input is activated."""
    #     anim = Animation(md_bg_color=(1, 0, 0, 1), duration=0.5) + \
    #            Animation(md_bg_color=App.get_running_app().theme_cls.primary_color, duration=0.5)
    #     anim.repeat = True
    #     anim.start(self.ids.voice_button)

    # def stop_voice_animation(self):
    #     """Stop animation when voice input ends."""
    #     Animation.cancel_all(self.ids.voice_button)
    #     self.ids.voice_button.md_bg_color = App.get_running_app().theme_cls.primary_color

    # def speech_to_text(self):
    #     """Convert speech to text and send message when speech stops."""
    #     recognizer = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         self.start_voice_animation()  # Start animation
    #         print("Listening... Speak now.")
    #         recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise

    #         try:
    #             # 🔥 Keep listening until the user stops speaking
    #             audio = recognizer.listen(source, phrase_time_limit=None)  
                
    #             # 🔥 Convert speech to text
    #             text = recognizer.recognize_google(audio)  
    #             print("You said:", text)
    #             self.ids.message_input.text = text  # Insert into input field
                
    #             # 🔥 Auto-send after speech stops
    #             self.send_message()

    #         except sr.UnknownValueError:
    #             print("Sorry, could not understand the audio.")
    #             self.ids.message_input.text = "Could not understand audio."

    #         except sr.RequestError:
    #             print("Could not request results. Check your internet connection.")
    #             self.ids.message_input.text = "Internet error. Try again."

    #         except sr.WaitTimeoutError:
    #             print("No speech detected. Try again.")
    #             self.ids.message_input.text = "No speech detected."

    #         self.stop_voice_animation()  # Stop animation

    def speech_to_text(self):
        """Convert speech to text and insert it into the chat input."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.start_voice_animation()  # Start animation
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjusts for background noise

            try:
                audio = recognizer.listen(source, timeout=5)  # Capture audio
                text = recognizer.recognize_google(audio)  # Convert to text
                print("You said:", text)
                self.ids.message_input.text = text  # Insert into input field

            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
                self.ids.message_input.text = "Could not understand audio."

            except sr.RequestError:
                print("Could not request results. Check your internet connection.")
                self.ids.message_input.text = "Internet error. Try again."

            except sr.WaitTimeoutError:
                print("No speech detected. Try again.")
                self.ids.message_input.text = "No speech detected."

            self.stop_voice_animation()  # Stop animation

class ChatbotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "AI Chat Assistant"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Dark"  # Default to dark theme

    def build(self):
        try:
            Window.size = (1200, 600)
            Window.minimum_width = 1000
            Window.minimum_height = 600
            
            # Create the screen manager
            sm = ScreenManager(transition=SlideTransition())
            
            # Add screens
            sm.add_widget(WelcomeScreen())
            sm.add_widget(SettingsScreen())
            sm.add_widget(ChatScreen())
            
            return sm
        except Exception as e:
            print(f"Error building app: {e}\n{traceback.format_exc()}")
            return None

    def switch_theme(self, is_dark):
        """Switch between light and dark themes"""
        self.theme_cls.theme_style = "Dark" if is_dark else "Light"
        print(f"Theme switched to: {self.theme_cls.theme_style}")

        if hasattr(self.root.get_screen('chat').ids, 'message_input'):
            input_field = self.root.get_screen('chat').ids.message_input

            text_color = [1, 1, 1, 1]  # White color
            hint_color = [0.7, 0.7, 0.7, 1]  # Light gray for hint
            
            # Set background color based on primary color
            if self.theme_cls.primary_palette == "Blue":
                fill_color = [0.12, 0.15, 0.33, 1]  # Dark blue background
            elif self.theme_cls.primary_palette == "Red":
                fill_color = [0.33, 0.12, 0.12, 1]  # Dark red background
            elif self.theme_cls.primary_palette == "Green":
                fill_color = [0.12, 0.33, 0.12, 1]  # Dark green background
            elif self.theme_cls.primary_palette == "Purple":
                fill_color = [0.25, 0.12, 0.33, 1]  # Dark purple background
            else:
                fill_color = [0.12, 0.12, 0.12, 1]  # Default dark background
            
    def change_primary_color(self, color_name):
        """Change the primary color palette"""
        self.theme_cls.primary_palette = color_name
        print(f"Primary color changed to: {color_name}")
        
        if hasattr(self.root.get_screen('chat').ids, 'message_input'):
            input_field = self.root.get_screen('chat').ids.message_input
        
        # Always white text
        text_color = [1, 1, 1, 1]
        hint_color = [0.7, 0.7, 0.7, 1]
        
        # Set background color based on new primary color
        if color_name == "Blue":
            fill_color = [0.12, 0.15, 0.33, 1]
        elif color_name == "Red":
            fill_color = [0.33, 0.12, 0.12, 1]
        elif color_name == "Green":
            fill_color = [0.12, 0.33, 0.12, 1]
        elif color_name == "Purple":
            fill_color = [0.25, 0.12, 0.33, 1]
        else:
            fill_color = [0.12, 0.12, 0.12, 1]
        
    def show_color_changed_notification(self, color_name):
        """Show a notification that color was changed"""
        try:
            from kivymd.uix.snackbar import Snackbar
            Snackbar(
                text=f"Primary color changed to {color_name}",
                md_bg_color=self.theme_cls.primary_color,
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.7
            ).open()
        except Exception as e:
            print(f"Could not show snackbar: {e}")

if __name__ == '__main__':
    try:
        print("Starting application...")
        ChatbotApp().run()
    except Exception as e:
        print(f"Application crashed: {e}\n{traceback.format_exc()}")    