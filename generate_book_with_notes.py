import sys, os
from subprocess import call

calibre_dir = "/Applications/calibre.app/Contents/console.app/Contents/MacOS/"

org_path = sys.argv[1]
book_dir, org_book_file = os.path.split(org_path)
book_name = os.path.splitext(org_book_file)[0]
htmlz_path = os.path.join(book_dir, book_name + '.htmlz')
call([os.path.join(calibre, "ebook-convert"), org_path, htmlz_path])


