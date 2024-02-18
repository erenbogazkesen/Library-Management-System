class Library:
 
  def __init__(self):
        self.file = open("books.txt", "a+")
   
  def listBooks(self): 
      
      try:
              with open("books.txt", 'r') as dosya:
                  # Dosyanın içeriğini satır bazında bir liste olarak oku
                  satir_listesi = dosya.read().splitlines()
                #  print(satir_listesi)
                 # print(satir_listesi[1].split(',')[0])
                  # Satırları ekrana yazdır
                  for satir in satir_listesi:
                      print(satir.split(',')[0]+" "+satir.split(',')[1])
                 # for indeks, satir in enumerate(satir_listesi):
                    # print(f"{satir.strip().split(',')[0]}")  
                   #  print(type(f"{satir.strip()}"))    
      except FileNotFoundError:
              print(f"{"books.txt"} adlı dosya bulunamadı.")
      except IOError:
              print("Dosya okuma sırasında bir hata oluştu.") 
  def addBooks(self):        
   try:
    # Dosyayı a+ modunda aç
      with open("books.txt", 'a+') as dosya:
        # Dosyanın var olup olmadığını kontrol et
        dosya.seek(0)
        icerik = dosya.read()
        if not icerik:
            print(f"{"books.txt"} adlı dosya bulunamadı. Yeni dosya oluşturuluyor.")
        else:
            print(f"{"books.txt"} adlı dosya zaten mevcut.")

        # Kullanıcıdan yazılacak metni al
        bilgiler = ["title", "author", "release year", "number of pages"]
        for index, bilgi in enumerate(bilgiler):
            metin = input(f"Enter the {bilgi}: ")
            dosya.write(metin)
            if index != len(bilgiler) - 1:  # Son bilgi değilse
                dosya.write(',')
            else:
              dosya.write('\n')
        print(f"{"books.txt"} adlı dosyaya metin eklendi.")
   except IOError:
     print("Dosya işlemi sırasında bir hata oluştu.")

  def removeBooks(self):
     silinmek_istenilen_kitap= input("Hangi kitabı silmek istiyorsunuz ")
     print(silinmek_istenilen_kitap)
     try:
    # Dosyayı aç ve satırları oku
        with open("books.txt", 'r') as dosya:
         satirlar = dosya.readlines()

    # Her satırın indeksini ve içeriğini ekrana yazdır
        for indeks, satir in enumerate(satirlar):
       #  print(f"{satir.strip()}")  # strip() metodu ile satır sonundaki boşlukları kaldırırız
         yeni_satirlar = [satir for indeks, satir in enumerate(satirlar)
                       if silinmek_istenilen_kitap != satir.strip().split(',')[0]]
         with open("books.txt", 'w') as dosya:
                dosya.writelines(yeni_satirlar)          
     except FileNotFoundError:
        print(f"{"books.txt"} adlı dosya bulunamadı.")
     except IOError:
          print("Dosya okuma sırasında bir hata oluştu.")   

  def __del__(self):
        self.file.close()  

lib = Library()
#lib.addBooks()
lib.listBooks()
#lib.removeBooks()   
lib.listBooks()

