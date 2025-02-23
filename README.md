
This script `app.py` will prompt the user for 
① PDF file
② Image destination directory
③ Markdown file destination directory
and create a Markdown file with each page of the pdf as a referenced image on its own line

(!) Caution: If using the "Paste image rename" Community plugin in Obsidian, it **must be disabled** as it will rename the image filenames when the script tries to write them to the markdown file.

The script parameters can either be passed in via the command line as arguments, or if nothing is passed in it will prompt the user with tkinter dialogues.

Example usage via command line:
`python app.py -input_pdf /path/to/file.pdf -image_output_folder /path/to/destimagedir -markdown_output_folder /path/to/filedestdir --quality 60 --viewsize 350`

Otherwise if just called as `python app.py`it will prompt the user for ①, ②, ③ in that order.

Use `python app.py -h` for argument descriptions

## Building

(Note tested on macOS Ventura 13.1 with anaconda 22.11.1 and python 3.10)

Download conda

Install dependencies using provided `environment.yml` which will create new environment named `parse-pdf-to-markdown`

`conda env create -f environment.yml`

Activate

`conda activate parse-pdf-to-markdown`

Run the test script (note you may need to add executable permissions e.g. `chmod +x test.sh`)

`./test.sh`


## Testing 

See the sandbox vault in `sandbox`

In `test.sh` replace variables for testing and run `./test.sh`
Clean sandbox vault manually with `./clean.sh`

Note we should surround bash variables in quotes in case there are spaces in the filename e.g.:

```
INPUT="vault/200-Courses/227B-MIT-6002-2-EdX/01B-Lecture-Slides-Annotated/W2-2-capacitors-first-order-annotated.pdf"

python app.py -i "$INPUT" \
-d "vault/z_attachments" \
-o "vault/200-Courses/227B-MIT-6002-2-EdX/01C-Lecture-Slides-MD-Images" \
--quality 60 --viewsize 350
```
