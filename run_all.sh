source ~/venv/bin/activate
parallel --keep-order "streamlit run week_0{}/Week_{}.py" ::: 1 2 3 4 5 6