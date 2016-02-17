import sys, os, subprocess
from get_notes import get_notes
from insert_notes import insert_notes

calibre_dir = "/Applications/calibre.app/Contents/console.app/Contents/MacOS/"
FNULL = open(os.devnull, 'w')

org_path = sys.argv[1]
book_dir, org_book_file = os.path.split(org_path)
book_name = os.path.splitext(org_book_file)[0]
htmlz_path = os.path.join(book_dir, book_name + '.htmlz')
tmp_dir = os.path.join(book_dir, book_name + "_tmp")
# subprocess.call(["rm", htmlz_path], stdout=FNULL, stderr=FNULL)
# subprocess.call([os.path.join(calibre_dir, "ebook-convert"), org_path, htmlz_path])
subprocess.call(["rm", "-rf", tmp_dir], stdout=FNULL, stderr=FNULL)
subprocess.call(["unzip", htmlz_path, "-d", tmp_dir], stdout=FNULL)

# now deal with the html format
notes = get_notes(book_name)
insert_notes(notes, tmp_dir)
new_htmlz_path = os.path.join(tmp_dir, book_name + '_with_notes.htmlz')
subprocess.call(["rm", new_htmlz_path], stdout=FNULL, stderr=FNULL)
print new_htmlz_path
os.system(subprocess.list2cmdline(["cd", tmp_dir, "&&",
	"zip", "-r", new_htmlz_path, "*"]))
new_mobi_path = os.path.join(book_dir, book_name + '_with_notes.mobi')
subprocess.call(["rm", new_mobi_path], stdout=FNULL, stderr=FNULL)
subprocess.call(
	[os.path.join(calibre_dir, "ebook-convert"), new_htmlz_path, new_mobi_path])
subprocess.call(["rm", htmlz_path], stdout=FNULL, stderr=FNULL)
# subprocess.call(["rm", "-rf", tmp_dir], stdout=FNULL, stderr=FNULL)


