from werkzeug.datastructures import FileStorage

def get_file_size (file: (FileStorage | None)): 
    if file:
        pos = file.stream.tell()
        file.stream.seek(0, 2)  # pindah ke akhir file
        file_size = file.stream.tell()  # posisi pointer di akhir = ukuran file
        file.stream.seek(pos)  # kembalikan posisi pointer ke awal

        return file_size