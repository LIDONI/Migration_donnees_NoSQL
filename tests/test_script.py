                              #---------------------------------------------------#
                              #    EXECUTION DES TESTS AUTOMATISES AVEC PYTEST    #
                              #---------------------------------------------------#
import subprocess
import sys

def run_all_tests():    # Fonction de lancement des test unitaires via pytest
   
    try:
        subprocess.check_call([
            sys.executable, "-m", "pytest", "tests/test_migration.py",
            "--maxfail=1", "--disable-warnings", "-v"
        ])
    except subprocess.CalledProcessError as e:
        print(f"\n Échec des tests. Code de retour : {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    run_all_tests()
