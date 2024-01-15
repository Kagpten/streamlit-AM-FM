import numpy as np
import pandas as pd
import streamlit as st

def sinyal_informasi(A_m, f_m, t):
    sinyal_informasi = A_m * np.cos(2 * np.pi * f_m * t)
    return pd.DataFrame({"Waktu (s)": t, "Amplitudo Informasi (V)": sinyal_informasi})

def sinyal_pembawa(A_c, f_c, t):
    sinyal_pembawa = A_c * np.cos(2 * np.pi * f_c * t)
    return pd.DataFrame({"Waktu (s)": t, "Amplitudo Pembawa (V)": sinyal_pembawa})

def sinyal_modulasi(A_m, f_m, A_c, f_c, indeks_modulasi, t):
    sinyal_informasi = A_m * np.cos(2 * np.pi * f_m * t)
    sinyal_pembawa = A_c * np.cos(2 * np.pi * f_c * t)
    sinyal_AM = A_c * (1 + indeks_modulasi * np.cos(2 * np.pi * f_m * t)) * np.cos(2 * np.pi * f_c * t)
    return pd.DataFrame({"Waktu (s)": t, "Amplitudo Informasi (V)": sinyal_informasi, "Amplitudo Pembawa (V)": sinyal_pembawa, "Modulasi Amplitudo (V)": sinyal_AM})

def sinyal_modulasi_frek(A_c, f_c, A_m, f_m, t):
    informasiInt = -np.cos(2 * np.pi * f_m * t)
    freqMod = A_c * np.sin(2 * np.pi * f_c * t + 2 * np.pi * 1 * informasiInt)
    return pd.DataFrame({"Waktu (s)": t, "Amplitudo Pembawa (V)": A_c * np.sin(2 * np.pi * f_c * t),
                         "Amplitudo Informasi (V)": A_m * np.sin(2 * np.pi * f_m * t),
                         "Modulasi Frekuensi (V)": freqMod})

# tampilan streamlit
st.title('Simulasi Modulasi')
st.title('Amplitudo dan Frekuensi')

st.caption('Dibuat oleh : ARILA RANGGA ALRASYID | 11-2021-008')
st.caption('Dosen Pembimbing : Ir. Rustamaji, M.T.')
st.caption('Mata Kuliah : Dasar Telekomunikasi')

# Pilihan jenis modulasi
modulasi_type = st.radio("Pilih jenis modulasi:", ["Amplitudo", "Frekuensi"])

# input parameter
A_m = st.number_input('Masukan Amplitudo Informasi (V)', min_value=0.1, max_value=10.0, step=0.1, value=1.0)
f_m = st.number_input('Masukan Frekuensi Informasi (s)', min_value=1.0, max_value=100.0, step=1.0, value=5.0)
A_c = st.number_input('Masukan Amplitudo Pembawa (V)', min_value=1.0, max_value=10.0, step=0.1, value=5.0)
f_c = st.number_input('Masukan Frekuensi Pembawa (s)', min_value=1.0, max_value=100.0, step=1.0, value=50.0)
t = np.linspace(0, 1, 1000)

if modulasi_type == "Amplitudo":
    indeks_modulasi = A_m / A_c
    sinyal_info = sinyal_informasi(A_m, f_m, t)
    sinyal_pem = sinyal_pembawa(A_c, f_c, t)
    sinyal_mod = sinyal_modulasi(A_m, f_m, A_c, f_c, indeks_modulasi, t)
else:
    sinyal_pem = sinyal_pembawa(A_c, f_c, t)
    sinyal_info = sinyal_informasi(A_m, f_m, t)
    sinyal_mod = sinyal_modulasi_frek(A_c, f_c, A_m, f_m, t)

# Create a pandas DataFrame
df = pd.DataFrame({'Waktu (s)': t, 'Amplitudo Informasi (V)': sinyal_info["Amplitudo Informasi (V)"],
                   'Amplitudo Pembawa (V)': sinyal_pem["Amplitudo Pembawa (V)"],
                   'Modulasi (V)': sinyal_mod["Modulasi Amplitudo (V)" if modulasi_type == "Amplitudo" else "Modulasi Frekuensi (V)"]})

# Display the dataframe in Streamlit
st.header("Sinyal Informasi")
st.line_chart(sinyal_info, x='Waktu (s)', y='Amplitudo Informasi (V)')
st.header("Sinyal Pembawa")
st.line_chart(sinyal_pem, x='Waktu (s)', y='Amplitudo Pembawa (V)')
st.header(f"Sinyal Modulasi {modulasi_type}")
st.line_chart(sinyal_mod, x='Waktu (s)', y=f"Modulasi {'Amplitudo' if modulasi_type == 'Amplitudo' else 'Frekuensi'} (V)")

st.latex(r'''
    V_m(t) = A_m \cos(2 \pi f_m t)
    ''')

st.latex(r'''
    V_c(t) = A_c \cos(2 \pi f_c t)
    ''')

if modulasi_type == "Amplitudo":
    st.latex(r'''
        V_{\text{AM}}(t) = A_c \left(1 + \frac{A_m}{A_c} \cos(2 \pi f_m t)\right) \cos(2 \pi f_c t)
        ''')
else:
    st.latex(r'''
        V_{\text{FM}}(t) = A_c \cos\left(2 \pi f_c t + m_f \cos(2 \pi f_m t)\right)
        ''')


st.write(df)

st.balloons()
