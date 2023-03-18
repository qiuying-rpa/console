cmd /c "python -m virtualenv venv"
cmd /c "venv\Scripts\activate & pip install -r requirements.txt"
rd /s /q static
rd /s /q templates
md templates
md static
git clone https://github.com/qiuying-rpa/designer.git
cd designer
cmd /c "pnpm i & pnpm build"
cd ..
move designer\dist\index.html templates\
move designer\dist\assets static\
move designer\dist\* static\
rd /s /q designer
flask run
