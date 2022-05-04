# Saya Silmi Aulia Rohmah mengerjakan TP 3 DPBO 2022 C1 
# dalam mata kuliah DPBO untuk keberkahanNya maka saya tidak melakukan 
# kecurangan seperti yang telah dispesifikasikan. Aamiin

from tkinter import *
import mysql.connector
from tkinter import ttk
from PIL import ImageTk, Image

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_dpbo_tp3"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.geometry("550x300")
    top.title("Input")

    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, ipadx=100, pady=10, ipady=100)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=50) # input nama
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=50) #input nim
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"] #list option jurusan
    input_jurusan = StringVar(root) 
    input_jurusan.set(options[0]) #set option pertama dengan list ke 0
    label3 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input3 = OptionMenu(dframe, input_jurusan, *options) # buat input option jurusan
    input3.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    #input 4

    input_gender = StringVar()
    input_gender.set("Laki-laki") #set checked radio button pertama dengan laki-laki

    label4 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")

    # input radio button gender
    Radiobutton(dframe, text="Laki-laki", variable=input_gender, value="Laki-laki").place(x=118,y=128)
    Radiobutton(dframe, text="Perempuan", variable=input_gender, value="Perempuan").place(x=220,y=128)
    
    #input 5

    label5 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    hobi = ["Bernyanyi", "Main game", "Jalan-jalan", "Baca buku", "Nonton", "Ngoding"] #list hobi

    input_hobi = ttk.Combobox(dframe, value=hobi) # input combo box
    input_hobi.current(0) # set current combo box pada list ke 0
    input_hobi.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, input_gender, input_hobi), top.withdraw()])
    btn_submit.grid(row=30, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=30, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, gender, hobi):
    
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    gender = gender.get()
    hobi = hobi.get()

    msg = []

    #cek apakah semua input sudah terisi
    if len(nama) == 0:
        msg.append('Nama tidak boleh kosong!')
    if len(nim) == 0:
        msg.append('NIM tidak boleh kosong!')
    if len(jurusan) == 0:
        msg.append('Jurusan tidak boleh kosong!')
    if len(gender) == 0:
        msg.append('Jenis kelamin tidak boleh kosong!')
    if len(hobi) == 0:
        msg.append('Hobi tidak boleh kosong!')
    
    
    top = Toplevel()

    if not msg: # jika list msg kosong // semua field input sudah terisi
        
        # buat query input data ke tabel
        sql = "INSERT INTO mahasiswa (nim, nama, jurusan, jenis_kelamin, hobi) VALUES (%s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, gender, hobi)

        dbcursor.execute(sql, val) # eksekusi
        mydb.commit()


        if(dbcursor.rowcount == 1): #jika data berhasil di insert ke dalam tabel
            Label(top, text="Berhasil menambahkan data").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        else: #jika data gagal insert ke tabel
            Label(top, text="Gagal menambahkan data").grid(row=0, column=0, padx=20, pady=10, sticky="w")

        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.grid(row=1, padx=10, pady=10)

    else: # jika list msg ada // terdapat field yang belum terisi

        #tampilkan pesan 
        i=0
        for pesan in msg:
            lbl = Label(top, text=pesan)
            lbl.grid(row=i+1, column=0, padx=20, pady=5, sticky="w")
            i += 1

        btn_ok = Button(top, text="OK", bg="green", fg="white", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.grid(row=i+1, padx=10, pady=10)

# Window Semua Mahasiswa
def viewAll():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():

    top = Toplevel()
    top.title("Delete All Record")

    # Buat query semua tabel mahasiswa
    sql = "DELETE FROM mahasiswa;"

    dbcursor.execute(sql) #eksekusi
    mydb.commit()

    banyakRecord = dbcursor.rowcount 

    if(banyakRecord > 0): #jika ada data yang berhasil dihapus
        msg = str(banyakRecord) + " record data dihapus"

        Label(top, text=msg).grid(row=0, column=0, padx=20, pady=10, sticky="w")

    else: #jika tidak ada data yang dihapus

        Label(top, text="Tidak ada record yang dihapus").grid(row=0, column=0, padx=20, pady=10, sticky="w")


    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.grid(row=1, column=0, padx=20, pady=10, sticky="s")

def facility():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")

    # menyimpan image fasilitas kampus
    img1 = ImageTk.PhotoImage(Image.open('images/ruang_kuliah.png'))
    img2 = ImageTk.PhotoImage(Image.open('images/perpustakaan.jpg'))
    img3 = ImageTk.PhotoImage(Image.open('images/masjid.png'))
    img4 = ImageTk.PhotoImage(Image.open('images/auditorium.jpg'))
    img5 = ImageTk.PhotoImage(Image.open('images/gymnasium.png'))
    img6 = ImageTk.PhotoImage(Image.open('images/pool.png'))

    image_list = [img1, img2, img3, img4, img5, img6] #buat list image

    frame = LabelFrame(top, borderwidth=0)
    frame.pack(padx=20, pady=20)

    label = Label(frame, text="Ruang Kelas", bd=1, relief=SUNKEN, anchor=S)

    my_label = Label(frame, image=img1)
    my_label.grid(row=0, column=0, columnspan=3)

    def forward(image_number): #fungsi untuk button next

        nonlocal my_label
        nonlocal button_forward
        nonlocal button_back

        my_label.grid_forget() # membuat widgets invisible
        #tampilkan image 
        my_label = Label(frame, image=image_list[image_number - 1])
        #tampilkan button next dan back 
        button_forward = Button(frame, text="Next", command=lambda: forward(image_number + 1))
        button_back = Button(frame, text="Back", command=lambda: back(image_number - 1))

        if image_number == 6:
            button_forward = Button(frame, text="Next", state=DISABLED) #jika current image pada nomor 6, buat button next disabled 

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_forward.grid(row=1, column=2)

        # buat label keterangan fasilitas setiap image 
        if image_number == 2:
            txt = "Perpustakaan"
        elif image_number ==3:
            txt = "Masjid"
        elif image_number ==4:
            txt = "Auditorium"
        elif image_number ==5:
            txt = "Gymnasium"
        elif image_number ==6:
            txt = "Kolam Renang"

        label = Label(frame, text=txt, bd=1, relief=SUNKEN, anchor=S)
        label.grid(row=2, column=0, columnspan=3, sticky=W+E)

    def back(image_number): #fungsi untuk button back

        nonlocal my_label
        nonlocal button_forward
        nonlocal button_back

        my_label.grid_forget() # membuat widgets invisible
        #tampilkan image 
        my_label = Label(frame, image=image_list[image_number - 1])
        #tampilkan button next dan back 
        button_forward = Button(frame, text="Next", command=lambda: forward(image_number + 1))
        button_back = Button(frame, text="Back", command=lambda: back(image_number - 1))

        if image_number == 1:
            button_back = Button(frame, text="Back", state=DISABLED) #jika current image pada nomor 1, buat button back disabled 

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_forward.grid(row=1, column=2)

        # buat label keterangan fasilitas setiap image 
        if image_number == 1:
            txt = "Ruang Kelas"
        elif image_number ==2:
            txt = "Perpustakaan"
        elif image_number ==3:
            txt = "Masjid"
        elif image_number ==4:
            txt = "Auditorium"
        elif image_number ==5:
            txt = "Gymnasium"
        elif image_number ==6:
            txt = "Kolam Renang"

        label = Label(frame, text=txt, bd=1, relief=SUNKEN, anchor=S)
        label.grid(row=2, column=0, columnspan=3, sticky=W+E)
    
    button_back = Button(frame, text="Back", command=lambda: back(), state=DISABLED)
    button_exit = Button(frame, text="Kembali Ke Menu Utama", command=lambda:[top.destroy(), root.deiconify()])
    button_forward = Button(frame, text="Next", command=lambda: forward(2))

    button_back.grid(row=1, column=0)
    button_exit.grid(row=1, column=1)
    button_forward.grid(row=1, column=2, pady=10)
    label.grid(row=2, column=0, columnspan=3, sticky=W+E)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

#Campus facility btn
b_clear = Button(buttonGroup, text="Tampilkan Daftar Fasilitas Kampus", command=facility, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()