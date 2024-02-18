import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color

class MyApp(App):
    def build(self):
        Window.bind(on_keyboard=self.on_key_down)
        self.bind(on_request_close=self.on_request_close)
        self.bind(on_key_down=self.on_key_down)

        primary_color = get_color_from_hex("#303F9F")  
        Window.clearcolor = primary_color  

        main_layout = BoxLayout(orientation='vertical')

        title_label = Label(text="Library Management System", font_size=30, size_hint=(1, 0.1))
        main_layout.add_widget(title_label)

        list_button = Button(text="List Books", size_hint=(1, 0.1))
        list_button.bind(on_press=self.show_book_list)
        main_layout.add_widget(list_button)

        add_button = Button(text="Add Book", size_hint=(1, 0.1))
        add_button.bind(on_press=self.show_add_book_popup)
        main_layout.add_widget(add_button)

        edit_button = Button(text="Edit Book", size_hint=(1, 0.1))
        edit_button.bind(on_press=self.show_edit_book_popup)
        main_layout.add_widget(edit_button)

        remove_button = Button(text="Remove Book", size_hint=(1, 0.1))
        remove_button.bind(on_press=self.show_remove_book_popup)
        main_layout.add_widget(remove_button)

        search_button = Button(text="Search", size_hint=(1, 0.1))
        search_button.bind(on_press=self.show_search_popup)
        main_layout.add_widget(search_button)

        return main_layout
    def on_keyboard(self, window, key, *args):
        if key == 113:  # ASCII kodu
            App.get_running_app().stop()
            return True  
        return False   

    def on_request_close(self, *args):
        
        return True

    def on_key_down(self, window, key, *args):
     if key == ord('q'):
        EventLoop.close()
        return True
     return False
    def show_add_book_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Book Title:"))
        book_title = TextInput(hint_text='Enter book title')
        content.add_widget(book_title)
        content.add_widget(Label(text="Author:"))
        author = TextInput(hint_text='Enter author name')
        content.add_widget(author)
        content.add_widget(Label(text="Release Year:"))
        release_year = TextInput(hint_text='Enter release year')
        content.add_widget(release_year)
        content.add_widget(Label(text="Number of Pages:"))
        num_pages = TextInput(hint_text='Enter number of pages')
        content.add_widget(num_pages)

        popup = Popup(title='Add Book', content=content, size_hint=(None, None), size=(400, 400))

        add_button = Button(text="Add", size_hint=(1, None), height=50)
        add_button.bind(on_press=lambda btn: self.add_book(popup, book_title.text, author.text, release_year.text, num_pages.text))
        content.add_widget(add_button)

        popup.open()

    def add_book(self, popup, title, author, release_year, num_pages):
    # Girişleri doğrulama
     errors = self.validate_input(title, author, release_year, num_pages)
     if errors:
        self.show_error_message("\n".join(errors))
        return

    
     dosya_adi = "books.txt"
     bilgiler = [title, author, release_year, num_pages]

     try:
        # Dosyaya bilgileri ekle
        with open(dosya_adi, 'a+') as dosya:
            dosya.write(','.join(bilgiler) + '\n')
        print(f"{dosya_adi} adlı dosyaya bilgiler eklendi.")
     except IOError:
        print("Dosya işlemi sırasında bir hata oluştu.")

     popup.dismiss()

    def show_book_list(self, instance):
     try:
        with open("books.txt", 'r') as dosya:
            book_info = [f"Book: {line.split(',')[0]}, Author: {line.split(',')[1]}" for line in dosya.readlines()]

        book_labels = [Label(text=info, size_hint_y=None, height=dp(50)) for info in book_info]

        book_grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        for label in book_labels:
            book_grid_layout.add_widget(label)

        # GridLayout'un minimum boyutunu hesapla
        book_grid_layout.bind(minimum_height=book_grid_layout.setter('height'))

        scroll_view = ScrollView()
        scroll_view.add_widget(book_grid_layout)

        self.popup = Popup(title='Book List', content=scroll_view, size_hint=(None, None), size=(400, 400))
        self.popup.open()
     except FileNotFoundError:
        print("books.txt adlı dosya bulunamadı.")
     except IOError:
        print("Dosya okuma sırasında bir hata oluştu.")


    def validate_input(self, title, author, release_year, num_pages):
        errors = []

       
        if not title:
            errors.append("Kitap adı boş bırakılamaz.")

       
        if not author:
            errors.append("Yazar adı boş bırakılamaz.")

        
        if not release_year.isdigit() or len(release_year) != 4:
            errors.append("Yayın yılı dört rakamdan oluşmalıdır.")

        if not num_pages.isdigit():
            errors.append("Sayfa sayısı bir tam sayı olmalıdır.")

        return errors

    def show_edit_book_popup(self, instance):
     content = BoxLayout(orientation='vertical')
     book_title_input = TextInput(hint_text='Enter book title')
     content.add_widget(Label(text="Book Title:"))
     content.add_widget(book_title_input)

     popup = Popup(title='Edit Book', content=content, size_hint=(None, None), size=(400, 200))

     edit_button = Button(text="Edit", size_hint=(1, None), height=50)
     edit_button.bind(on_press=lambda btn: self.edit_book(popup, book_title_input.text))
     content.add_widget(edit_button)

     popup.open()

    def edit_book(self, popup, title):
     print(f"Editing book: {title}") 
     

    
     book_title = title.strip()

     if not book_title:
        self.show_error_message("Please enter a book title.")
        return

     try:
        with open("books.txt", 'r') as file:
            lines = file.readlines()
            found = False

            for line in lines:
                parts = line.strip().split(',')
                if parts[0] == book_title:
                    found = True
                    break

            if found:
                self.edit_popup = Popup(title='Edit Book', size_hint=(None, None), size=(400, 400))
                edit_layout = BoxLayout(orientation='vertical')

                edit_layout.add_widget(Label(text="New Title:"))
                new_title_input = TextInput(text=parts[0], multiline=False)
                edit_layout.add_widget(new_title_input)

                edit_layout.add_widget(Label(text="New Author:"))
                new_author_input = TextInput(text=parts[1], multiline=False)
                edit_layout.add_widget(new_author_input)

                edit_layout.add_widget(Label(text="New Release Year:"))
                new_release_year_input = TextInput(text=parts[2], multiline=False)
                edit_layout.add_widget(new_release_year_input)

                edit_layout.add_widget(Label(text="New Number of Pages:"))
                new_num_pages_input = TextInput(text=parts[3], multiline=False)
                edit_layout.add_widget(new_num_pages_input)

                save_button = Button(text="Save", size_hint=(1, None), height=50)
                save_button.bind(on_press=lambda btn: self.save_book_edits(popup, new_title_input.text, new_author_input.text, new_release_year_input.text, new_num_pages_input.text))
                edit_layout.add_widget(save_button)

                self.edit_popup.content = edit_layout
                self.edit_popup.open()
            else:
                self.show_error_message("Book not found.")
     except FileNotFoundError:
        self.show_error_message("books.txt not found.")
     except Exception as e:
        self.show_error_message(f"An error occurred: {e}")

    def save_book_edits(self, popup, new_title, new_author, new_release_year, new_num_pages):
     print("Saving book edits...")
     try:
        # Dosyayı okuyup, değişiklikleri yaparak geçici bir listede saklayalım
        with open("books.txt", 'r') as file:
            lines = [line.strip().split(',') for line in file]

        for i, parts in enumerate(lines):
            if parts[0] == new_title:
                lines[i] = [new_title, new_author, new_release_year, new_num_pages]

        # Geçici listeyi dosyaya yazalım
        with open("books.txt", 'w') as file:
            for line in lines:
                file.write(','.join(line) + '\n')

        print("Book edits saved successfully.")
     except FileNotFoundError:
        self.show_error_message("books.txt not found.")
     except Exception as e:
        self.show_error_message(f"An error occurred: {e}")

     print("Trying to close popup...")
     popup.dismiss()


    def show_error_message(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_remove_book_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Book Title:"))
        book_title = TextInput(hint_text='Enter book title')
        content.add_widget(book_title)

        popup = Popup(title='Remove Book', content=content, size_hint=(None, None), size=(400, 200))

        remove_button = Button(text="Remove", size_hint=(1, None), height=50)
        remove_button.bind(on_press=lambda btn: self.remove_book(popup, book_title.text))
        content.add_widget(remove_button)

        popup.open()

    def remove_book(self, popup, title):
        print(f"Removing book: {title}")

        try:
            with open("books.txt", 'r') as dosya:
                satirlar = dosya.readlines()

            yeni_satirlar = [satir for satir in satirlar if title != satir.strip().split(',')[0]]

            with open("books.txt", 'w') as dosya:
                dosya.writelines(yeni_satirlar)

        except FileNotFoundError:
            print("books.txt adlı dosya bulunamadı.")
        except IOError:
            print("Dosya okuma/silme sırasında bir hata oluştu.")

        popup.dismiss()

    def show_search_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Search by Book Title:"))
        search_input = TextInput(hint_text='Enter book title')
        content.add_widget(search_input)

        popup = Popup(title='Search Books', content=content, size_hint=(None, None), size=(400, 200))

        search_button = Button(text="Search", size_hint=(1, None), height=50)
        search_button.bind(on_press=lambda btn: self.search_books(search_input.text))
        content.add_widget(search_button)

        popup.open()

    def search_books(self, search_text):
     if not search_text:
        self.show_error_message("Please enter a search query.")
        return
 
     try:
        with open("books.txt", 'r') as file:
            found_books = [line for line in file if search_text.lower() in line.lower().split(',')[0]]

        if found_books:
            self.show_search_results(found_books)
        else:
            self.show_error_message("No matching books found.")
     except FileNotFoundError:
        self.show_error_message("books.txt not found.")
     except Exception as e:
        self.show_error_message(f"An error occurred: {e}")


    def show_search_results(self, books):
        
        scroll_view = ScrollView()
        book_grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        for book in books:
            book_label = Label(text=book, size_hint_y=None, height=dp(50))
            scroll_view.add_widget(book_label)

        popup = Popup(title='Search Results', content=scroll_view, size_hint=(None, None), size=(400, 400))
        popup.open()
        book_grid_layout.bind(minimum_height=book_grid_layout.setter('height'))

        #scroll_view.add_widget(book_grid_layout)
    def show_error_message(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()    

if __name__ == '__main__':
    MyApp().run()
