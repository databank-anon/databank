apt-get install git ocaml opam libgmp-dev subversion python3-pip

git clone https://github.com/databank-anon/databank

opam init
eval $(opam env)
opam switch create 4.07.0
eval $(opam env)
opam install ocamlfind qcheck zarith
eval $(opam env)

cd databank/monpoly
make
cd ..
pip3 install -r requirements.txt
cd src
python3 main.py
