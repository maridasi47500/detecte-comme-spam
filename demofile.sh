
mkdir templates 
python3 scaffold.py email from to subject content status created_at
python3 scaffold.py user email password country_id:references phone username
python3 scaffold.py country name
python3 scaffold.py image email_id:references pic:file order
python3 scaffold.py attachment email_id:references attachment:file order
python3 scaffold.py text police taille couleur email_id:references order
