1. Nie wygenerowa�em jara, poniewa� wa�y� 12MB i zip nie chcia� za��czy� si� na isodzie.
2. Aby skompliowa� program nale�y:
 a) zaci�gn�� wszystkie dependencies z Mavena, pom.xml PPM -> Maven -> Reimport
 b) doda� linijk� --add-modules=java.se.ee w polu VM options w konfiguracji uruchamiania programu
3. W startowym okienku z podaniem nazwy u�ytkownika nale�y wpisa� login wybrany w aplikacji WEB (nie ma tutaj zrobionej autoryzacji, wystaczy sam login)
