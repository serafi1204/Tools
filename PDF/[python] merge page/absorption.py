import os
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation

# Load exercise page
exercisePageFileName = 'exercisePage.pdf'
while (True):
    try:
        exercisePage = PdfReader(exercisePageFileName, "rb").pages[0]
    except PermissionError:
        os.chmod(name, 0o777)
    else:
        break
    

# Get path
path = input('Enter path: ')
path = path.replace('\\', '/')
folderName = path.split('\\')[-1]

# Read folder
fileNames = os.listdir(path)
    
# Read file
PDFs = []
print("Found PDFs...")
for name in fileNames:
    if (name.split('.')[-1] == 'pdf'):
        while (True):
            try:
                PDFs.append([PdfReader(path+'\\'+name, "rb"), name])
            except PermissionError:
                os.chmod(name, 0o777)
            else:
                print(f'\t{name}')
                break
            
# Set parameter
offset = 10
width = PDFs[0][0].pages[0].mediabox.width*2
height = PDFs[0][0].pages[0].mediabox.height*2
    
#Absorption
print(f'Drawing new PDF...')
pdf = PdfWriter()

def insertPage(page, pageSub, x, y):
    tempPage = PageObject.create_blank_page(None, width+offset*3, height+offset*3)
    tempPage.merge_page(pageSub)
    tempPage.add_transformation(Transformation().scale(1).translate(x*width/2 + (x+1)*offset, y*height/2 + (y+1)*offset))    
    page.merge_page(tempPage)
    
    return page

for PDF in PDFs:
    paper, name = PDF
    
    if (len(paper.pages) != 3): print(f'Check # of page of {name}.')
        
    page = PageObject.create_blank_page(None, width+offset*3, height+offset*3)
    page = insertPage(page, paper.pages[0], 1, 1) 
    page = insertPage(page, exercisePage, 0, 1) 
    page = insertPage(page, paper.pages[1], 0, 0) 
    page = insertPage(page, paper.pages[2], 1, 0) 
    
    pdf.add_page(page)
    
    print(f'\tComplete page for {name}')    
    
# Save pdf
pdf.write(open(f"{folderName}.pdf", "wb"))
input('Complete whole process. Press any key.')

