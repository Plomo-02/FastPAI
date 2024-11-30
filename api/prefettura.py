import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class DataServizio:
    def __init__(
        self,
        titolo: str,
        giorni_liberi: List[str],
        info_orari: str,
        a_chi_si_rivolge: str,
        cosa_avere: List[str],
        misc_info: str,
    ):
        self.titolo = titolo
        self.giorni_liberi = giorni_liberi
        self.info_orari = info_orari
        self.a_chi_si_rivolge = a_chi_si_rivolge
        self.cosa_avere = cosa_avere
        self.misc_info = misc_info


class TribunaleDataExtractor:
    def __init__(self):
        self.endpoint_mapping: Dict[str, str] = {
            "tessera_a_te": "10000",
            "legalizzazionr_documenti": "560",
            "discarichi_cartelle": "561",
            "cittadinanza": "656",
            "revoca_patente_req_morali": "320",
            "registro_enti_culto": "568",
            "registro_persone_giuridiche": "569",
            "sospensione_patente_codice_strada": "247",
            "sospensione_patente_stupefacenti": "259",
        }

    def extract_title(self, soup: BeautifulSoup) -> str:
        titolo = soup.find("h1", class_="titoloServizio")
        if titolo:
            return titolo.get_text(strip=True)
        return ""

    def extract_dates_from_script(self, script_content: str) -> List[str]:
        dates = []
        lines = script_content.split("\n")
        for line in lines:
            if "SelectedDates.push('2024" in line:
                date = line.split("'")[1]
                dates.append(date)
        return dates

    def extract_info_orari(self, soup: BeautifulSoup) -> str:
        info_orari = soup.find("article", id="info-orari")
        if info_orari:
            return info_orari.get_text(strip=True)
        return ""

    def extract_a_chi_si_rivolge(self, soup: BeautifulSoup) -> str:
        a_chi_si_rivolge = soup.find("article", id="a-chi-si-rivolge")
        if a_chi_si_rivolge:
            return a_chi_si_rivolge.get_text(strip=True)
        return ""

    def extract_cosa_serve(self, soup: BeautifulSoup) -> List[str]:
        cosa_serve_div = soup.find("article", id="cosa-serve")
        if cosa_serve_div:
            cosa_serve_items = cosa_serve_div.find_all("p")
            return [item.get_text(strip=True) for item in cosa_serve_items]
        return []

    def extract_misc_info(self, soup: BeautifulSoup) -> str:
        cos_e_div = soup.find("article", id="cos-e")
        if cos_e_div:
            return cos_e_div.get_text(strip=True)
        return ""

    def _get_data_from_tribunale(self, endpoint: str) -> DataServizio:
        params = {
            "azione": "review_servizio_agenda",
            "id_servizio": endpoint,
        }

        response = requests.get(
            "https://prenotazioni.utgroma.it/ajax_ecomune.php", params=params
        )

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title
            titolo = self.extract_title(soup)

            # Extract dates from the script
            script_content = soup.find("script", type="text/javascript").string
            giorni_liberi = self.extract_dates_from_script(script_content)

            # Extract "info orari" information
            info_orari = self.extract_info_orari(soup)

            # Extract "a chi si rivolge" information
            a_chi_si_rivolge = self.extract_a_chi_si_rivolge(soup)

            # Extract "cosa-serve" information
            cosa_avere = self.extract_cosa_serve(soup)

            # Extract "misc info"
            misc_info = self.extract_misc_info(soup)

            return DataServizio(
                titolo,
                giorni_liberi,
                info_orari,
                a_chi_si_rivolge,
                cosa_avere,
                misc_info,
            )
        else:
            raise Exception(
                f"Failed to retrieve data for endpoint {endpoint}. Status code: {response.status_code}"
            )

    def get_data_from_tribunale(self, input_string: str) -> DataServizio:
        endpoint = self.endpoint_mapping.get(input_string)
        if not endpoint:
            raise ValueError(f"No endpoint found for input string: {input_string}")

        return self._get_data_from_tribunale(endpoint)


# How to use:
if __name__ == "__main__":
    try:
        extractor = TribunaleDataExtractor()
        data_servizio = extractor.get_data_from_tribunale("tessera_a_te")
        print("Titolo:", data_servizio.titolo)
        print("Giorni liberi:")
        for giorno in data_servizio.giorni_liberi:
            print(giorno)
        print(f"\nInfo orari:\n{data_servizio.info_orari}")
        print(f"\nA chi si rivolge:\n{data_servizio.a_chi_si_rivolge}")
        print("\nCosa avere:")
        for cosa in data_servizio.cosa_avere:
            print(cosa)
        print(f"\nMisc info:\n{data_servizio.misc_info}")
    except Exception as e:
        print(e)
