M-H algoritmus
==============

Python knihovna pro šifrování, dešifrování a kryptoanalýzu substituční šifry
pomocí Metropolis-Hastings algoritmu.

Python verze
------------------------------
Před spuštěním se ujistěte, že máte nainstalovaný Python 3.13.1 nebo vyšší.

```python -V```

Instalace balíčků
------------------------------
Pro instalaci potřebných balíčků použijte příkaz:

```pip install -r requirements.txt```

Spuštění M-H algoritmu
------------------------------
Přejděte do root složky projektu a zadejte příkaz:

```python -m MH_decipher.mh_algorithm```

Spuštění unit testů
------------------------------
Pro spuštění unit testů poté použijte tento příkaz v root složce projektu:

```python -m unittest discover -s MH_decipher/test -p "*.py"```