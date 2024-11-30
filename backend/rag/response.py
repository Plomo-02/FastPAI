
def send_response(self, query: str, result: str) -> str:
    """Invia una richiesta al modello OpenAI."""
    user_content = f"""Richiesta originale dell'utente: {query}
                     Risposta dal database vettoriale: {result}"""
    
    response = self.client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Modello utilizzato
        messages=[
            {"role": "system", "content": """Sei un assistente esperto di comunicazione chiara e accessibile per i cittadini. Ricevi una risposta da un database vettoriale contenente dati come città, date, orari disponibili e altre informazioni, insieme alla richiesta originale dell'utente. Il tuo compito è formulare una risposta semplice, chiara, concisa e facilmente comprensibile da qualunque cittadino, mantenendo solo le informazioni più rilevanti."""},
            {"role": "user", "content": user_content}
        ],
        max_tokens=128
    )
    return response.choices[0].message.content.strip()



def format_response(query,result):
    llm_response = send_response(query,result)
    """
    implement the response formatting here, to obtain date e orari disponibili, e info 
    """

    result_json = {"llm_response": llm_response, "results": result}
    return result_json