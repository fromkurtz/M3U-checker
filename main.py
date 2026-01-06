import requests
import os
import glob

# --- CONFIGURAÇÕES ---
CAMINHO_PASTA = r'C:\Caminho\Para\Suas\Listas' # Use 'r' antes das aspas no Windows
ARQUIVO_SAIDA = 'lista_consolidada_online.m3u8'
TIMEOUT = 5 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def validar_iptv():
    canais_unicos = {} # Dicionário para evitar duplicatas de (Nome + URL)
    
    # Ajusta o caminho para buscar os arquivos
    padrao_busca = os.path.join(CAMINHO_PASTA, "*.m3u*")
    arquivos_m3u = glob.glob(padrao_busca)
    
    if not arquivos_m3u:
        print(f"Nenhum arquivo encontrado em: {CAMINHO_PASTA}")
        return

    print(f"--- Encontrados {len(arquivos_m3u)} arquivos para processar ---")

    for arquivo in arquivos_m3u:
        # Ignora o arquivo de saída se ele estiver na mesma pasta
        if ARQUIVO_SAIDA in arquivo:
            continue
            
        print(f"\nLendo: {os.path.basename(arquivo)}")
        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            continue

        nome_metadata = ""
        for linha in linhas:
            linha = linha.strip()
            
            if linha.startswith('#EXTINF'):
                nome_metadata = linha
            
            elif linha.startswith('http'):
                url = linha
                # Cria uma chave única baseada no nome limpo e na URL
                # Isso evita nomes iguais com links diferentes e vice-versa
                chave_duplicata = f"{nome_metadata}_{url}"
                
                if chave_duplicata not in canais_unicos:
                    try:
                        # Verifica se o link responde
                        response = requests.head(url, timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
                        
                        if response.status_code == 200:
                            print(f"  [ON]  {url}")
                            canais_unicos[chave_duplicata] = (nome_metadata, url)
                        else:
                            print(f"  [OFF] Status {response.status_code}")
                            
                    except Exception:
                        print(f"  [OFF] Timeout/Erro")
                else:
                    print(f"  [SKIP] Canal/Link já processado")

    # Salva o arquivo final
    caminho_final = os.path.join(CAMINHO_PASTA, ARQUIVO_SAIDA)
    with open(caminho_final, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for nome, url in canais_unicos.values():
            f.write(f"{nome}\n{url}\n")
    
    print(f"\n" + "="*40)
    print(f"PROCESSO CONCLUÍDO!")
    print(f"Canais Online e Únicos: {len(canais_unicos)}")
    print(f"Salvo em: {caminho_final}")
    print("="*40)

if __name__ == "__main__":
    validar_iptv()