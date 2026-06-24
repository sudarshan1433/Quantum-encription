import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from cryptography.fernet import Fernet
import base64
import hashlib
import os

st.set_page_config(page_title="Quantum-Shield Vault", page_icon="🛡️")
st.title("🛡️ Quantum-Shield Vault")
st.write("Quantum-safe encryption tool.")

# --- 1. Quantum Key Generation (Only Once) ---
st.subheader("1. Chabi (Key) Banayein")
st.write("Pehle ek solid Quantum Key generate karein aur use copy kar lein.")

if st.button("🔑 Generate Quantum Key"):
    # Quantum Superposition se true randomness nikalna
    qc = QuantumCircuit(8, 8)
    qc.h(range(8))
    qc.measure(range(8), range(8))
    
    sim = AerSimulator()
    job = sim.run(qc, shots=1)
    q_bits = list(job.result().get_counts().keys())[0]
    
    # Quantum bits aur random salt ko milakar ek unbreakable 256-bit key banana
    random_salt = os.urandom(16)
    combined_entropy = f"quantum_{q_bits}".encode() + random_salt
    hash_key = hashlib.sha256(combined_entropy).digest()
    final_key = base64.urlsafe_b64encode(hash_key).decode()
    
    st.success("Aapki Quantum Key taiyar hai! Ise COPY karke notes mein save kar lein:")
    st.code(final_key, language='text')
    st.warning("Dhyan rahe: Agar yeh key ghum gayi, toh data kabhi wapas nahi aayega!")

st.divider()

# --- 2. Encrypt & Decrypt Logic ---
st.subheader("2. Data Lock / Unlock Karein")
user_key = st.text_input("Apni Quantum Key yahan paste karein:", type="password")

if user_key:
    try:
        cipher_suite = Fernet(user_key.encode())
        action = st.radio("Aap kya karna chahte hain?", ("Data Encrypt (Lock)", "Data Decrypt (Unlock)"))
        
        if action == "Data Encrypt (Lock)":
            raw_text = st.text_area("Apna Secret Message yahan likhein:")
            if st.button("🔒 Encrypt Data"):
                if raw_text:
                    encrypted_text = cipher_suite.encrypt(raw_text.encode()).decode()
                    st.success("Data Lock ho gaya hai!")
                    st.code(encrypted_text, language='text')
                else:
                    st.error("Pehle message likhein!")

        elif action == "Data Decrypt (Unlock)":
            enc_text = st.text_area("Apna Encrypted Data yahan paste karein:")
            if st.button("🔓 Decrypt Data"):
                if enc_text:
                    decrypted_text = cipher_suite.decrypt(enc_text.encode()).decode()
                    st.success("Data Unlock ho gaya!")
                    st.info(decrypted_text)
                else:
                    st.error("Pehle Encrypted data paste karein!")
    except ValueError:
        st.error("❌ Galat format! Kripya sahi Quantum Key paste karein.")
    except Exception as e:
        st.error("❌ Decryption Fail! Key ya Encrypted Data galat hai.")
