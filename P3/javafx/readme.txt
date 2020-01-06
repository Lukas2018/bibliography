1. Nie wygenerowa³em jara, poniewa¿ wa¿y³ 12MB i zip nie chcia³ za³¹czyæ siê na isodzie.
2. Aby skompliowaæ program nale¿y:
 a) zaci¹gn¹æ wszystkie dependencies z Mavena, pom.xml PPM -> Maven -> Reimport
 b) dodaæ linijkê --add-modules=java.se.ee w polu VM options w konfiguracji uruchamiania programu
3. W startowym okienku z podaniem nazwy u¿ytkownika nale¿y wpisaæ login wybrany w aplikacji WEB (nie ma tutaj zrobionej autoryzacji, wystaczy sam login)
