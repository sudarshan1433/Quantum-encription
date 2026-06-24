import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from cryptography.fernet import Fernet
import base64
import hashlib

# --- Page Setup ---
st.set_page_config(page_title="Quantum-Shield Vault", page_icon="🛡️")
st.title("🛡️ Quantum-Shield Vault")
st.write("Aapke data ko future-proof aur Quantum-safe banane wala security tool.")

# --- Logic: Quantum Key Generation ---
def generate_quantum_key(user_seed):
    """
    Qiskit ka use karke ek random aur complex key banana.
    (Note: Fast user experience ke liye hum AerSimulator use kar rahe hain. 
    Real IBM hardware par queue ki wajah se ghanton lag sakte hain).
    """
    qc = QuantumCircuit(8, 8)
    qc.h(range(8)) # Qubits ko superposition mein daalna
    qc.measure(range(8), range(8))
    
    sim = AerSimulator()
    job = sim.run(qc, shots=1)
    counts = job.result().get_counts()
    
    quantum_bits = list(counts.keys())[0]
    
    # Quantum bits aur user ke secret word ko milakar ek unbreakable 256-bit key banana
    combined_entropy = f"{quantum_bits}_{user_seed}".encode()
    hash_key = hashlib.sha256(combined_entropy).digest()
    return base64.urlsafe_b64encode(hash_key)

# --- App UI ---
st.subheader("1. Quantum Key Generate Karein")
user_secret = st.text_input("Apna koi Secret Word ya PIN daalein (ise yaad rakhna zaroori hai!):", type="password")

if user_secret:
    q_key = generate_quantum_key(user_secret)
    cipher_suite = Fernet(q_key)
    
    action = st.radio("Aap kya karna chahte hain?", ("Data Encrypt (Lock)", "Data Decrypt (Unlock)"))
    
    if action == "Data Encrypt (Lock)":
        raw_text = st.text_area("Apna Secret Message ya Password yahan likhein:")
        if st.button("🔒 Encrypt Data"):
            if raw_text:
                encrypted_text = cipher_suite.encrypt(raw_text.encode()).decode()
                st.success("Data Quantum Key se lock ho gaya hai!")
                st.code(encrypted_text, language='text')
                st.warning("Upar diye gaye Encrypted text ko copy karke safe rakh lein.")
            else:
                st.error("Pehle message likhein!")

    elif action == "Data Decrypt (Unlock)":
        enc_text = st.text_area("Apna Encrypted Data yahan paste karein:")
        if st.button("🔓 Decrypt Data"):
            if enc_text:
                try:
                    decrypted_text = cipher_suite.decrypt(enc_text.encode()).decode()
                    st.success("Data Unlock ho gaya!")
                    st.info(decrypted_text)
                except Exception as e:
                    st.error("Galat Secret Word ya Corrupted Data! Decryption Fail.")
            else:
                st.error("Pehle Encrypted data paste karein!")

