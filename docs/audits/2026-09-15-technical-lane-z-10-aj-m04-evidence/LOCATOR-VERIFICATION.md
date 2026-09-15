Consumers: `[#784]` (the row this evidence serves), `[#696]` (the locator defect it answers)

# locator verification against AJ_M04_transkrypcje.md
# items: 82 | EXACT: 2 | NORM: 80

[01] NORM lesson=L01 stated=17-19 found=17 kind=architecture
     ITEM: Maintain an architectural separation of concerns where MCP defines the tool request format while the application independently manages the model and tool invocation logic.
     QUOTE: MCP definiuje format danych, czyli to, jak model ma prosić narzędzia, ale nie narzuca aplikacji, jak ma zarządzać modelem albo jak agent i kiedy powinien wywoływać dane narzędzia.

[02] NORM lesson=L01 stated=59-61 found=59 kind=architecture
     ITEM: Implement connection management, user consent prompts, and authorization flows when building an enterprise chatbot that acts as an MCP Host.
     QUOTE: Czyli to Wy będziecie musieli zaimplementować i zdecydować, jak zarządzać wieloma połączeniami, jak pytać użytkowników o zgodę, jak zarządzać autoryzacją.

[03] NORM lesson=L01 stated=111-112 found=111 kind=lifecycle
     ITEM: Re-establish the connection with a new handshake if you need to use capabilities that were not declared initially.
     QUOTE: nie ma możliwości, żeby zacząć obsługiwać te obrazki bez nawiązania ponownego połączenia, czyli bez ponownego Handshake'u.

[04] NORM lesson=L01 stated=112-113 found=112 kind=lifecycle
     ITEM: Adhere strictly to the capabilities and versions negotiated during the initial handshake, as they remain fixed for the entire duration of the session.
     QUOTE: To, co zostanie wynegocjowane tutaj, jest wiążące przez całą sesję.

[05] NORM lesson=L02 stated=153-154 found=153 kind=practice
     ITEM: Provide descriptions for both the tool itself and its input/output schema when defining it.
     QUOTE: przy definicji narzędzia bardzo ważne są dwie rzeczy. Oczywiście to jest opis schematu wejściowego, wyjściowego danego narzędzia, ale też opis tego narzędzia.

[06] NORM lesson=L02 stated=155-157 found=155 kind=practice
     ITEM: Describe the tool's function and its parameters clearly and thoroughly to minimize the chance of the model hallucinating its usage or inputs.
     QUOTE: im lepiej opiszesz, co robi dana funkcja, im lepiej opiszesz, jakie są jej parametry, tym rzadziej model będzie halucynował moment jej użycia bądź halucynował wejściowe parametry.

[07] NORM lesson=L02 stated=159-162 found=159 kind=capability
     ITEM: Include contextual hints like readOnlyHint or destructiveHint to inform the model about the nature and side effects of the tool.
     QUOTE: Możemy też dodawać pewne podpowiedzi dotyczące charakteru danego narzędzia, tak jak np. readOnlyHint, który mówi, że to narzędzie nie ma żadnych skutków ubocznych, albo destructiveHint, że to narzędzie może usuwać dane.

[08] NORM lesson=L02 stated=184-186 found=184 kind=practice
     ITEM: Include a serialized text string in the content field as a fallback, even when returning data in the StructuredContent format.
     QUOTE: nawet jeżeli wysyłacie dane w tym takim nowoczesnym, można powiedzieć, formacie StructuredContent, to dla klientów i tak często musimy zwracać tą wersję tekstową w formie content.

[09] NORM lesson=L02 stated=195-197 found=195 kind=anti-pattern
     ITEM: Avoid returning JSON-RPC protocol-level errors for application-level issues, such as a missing database record.
     QUOTE: jeżeli np. narzędzie nie znajdzie jakiegoś użytkownika w bazie, to nie powinniście zwracać błędu na poziomie protokołu JSON-RPC, bo błąd protokołu jako taki jest błędem krytycznym.

[10] NORM lesson=L02 stated=198-199 found=198 kind=practice
     ITEM: Communicate application-level errors by returning a standard response and setting the isError field to true.
     QUOTE: Zamiast tego powinien się zwrócić normalny wynik, natomiast pole isError ustawić na true.

[11] NORM lesson=L02 stated=244-247 found=244 kind=capability
     ITEM: Push a notifications/resources/updated message from the server when you want the client to refresh live resources without waiting for a user action.
     QUOTE: serwer może wysyłać taką notyfikację notifications/resources/updated, co jest na przykład idealne, jak chcecie monitorować logi na żywo.

[12] NORM lesson=L02 stated=249-250 found=249 kind=architecture
     ITEM: Do not use resources as an unlimited storage mechanism, as language models have finite context windows.
     QUOTE: jako architekci musimy pamiętać, że zasoby to nie jest nielimitowany dysk.

[13] NORM lesson=L02 stated=256-257 found=256 kind=practice
     ITEM: Serve granular, essential fragments of data using templates instead of returning massive, unoptimized data dumps.
     QUOTE: używamy template'ów tam, gdzie możemy, żeby serwować tylko małe, te niezbędne fragmenty danych, a nie całe wielkie dumpy.

[14] NORM lesson=L02 stated=258-259 found=258 kind=capability
     ITEM: Implement pagination with parameters to allow the model to fetch and scroll through long lists piece by piece.
     QUOTE: możemy stosować paginację, czyli jeśli lista jest za długa, to mamy parametr, który pozwala modelowi przewijać kawałek po kawałku te komponenty.

[15] EXACT lesson=L02 stated=261 found=261 kind=practice
     ITEM: Be highly cautious with binary data, as it consumes context capacity much faster than lines of code.
     QUOTE: Pamiętajmy też, że dane binarne bardzo zżerają kontekst.

[16] NORM lesson=L02 stated=265-267 found=265 kind=practice
     ITEM: Expose a specific tool for searching large datasets instead of relying on the AI to locate information within a bulk resource.
     QUOTE: jeżeli chcesz, żeby AI przeszukała jakiś wielki zbiór danych, to utwórz do tego narzędzie, czyli użyj Tools, a nie licz, że odnajdzie to w zasobie.

[17] NORM lesson=L02 stated=273-275 found=273 kind=architecture
     ITEM: Rely predominantly on tools for interaction to ensure the server-host communication remains visible and available to the model within the chat window.
     QUOTE: w przypadku MCP musimy opierać się maksymalnie na narzędziach, żeby ta interakcja MCP Server z MCP Host w maksymalnym stopniu była dostępna w danym oknie czatu i była dostępna dla modelu.

[18] NORM lesson=L02 stated=292-293 found=292 kind=lifecycle
     ITEM: Send a PromptListChanged notification after updating a prompt so the host can refresh the logic immediately without requiring a connection restart.
     QUOTE: jeżeli chcemy zmienić sposób, w jaki agent obsługuje błędy, aktualizujemy ten prompt i wysyłamy powiadomienie PromptListChanged

[19] NORM lesson=L02 stated=320-322 found=319 kind=capability
     ITEM: Utilize MCP Apps rather than Tools when the output requires user interactions such as clicking, filtering data, or submitting forms.
     QUOTE: Jeżeli wynik wymaga od użytkownika klikania, filtrowania danych, wypełniania formularzy, no to App będzie, najprawdopodobniej, bo jest to dość nowy standard, lepsze od Tools

[20] NORM lesson=L02 stated=343-345 found=343 kind=security
     ITEM: Filter Sampling requests on the host to ensure the server cannot maliciously extract confidential data from the chat history.
     QUOTE: MCP Host ma tak na to obowiązek filtrować te prośby o Sampling, żeby serwer nie próbował na przykład wyłudzać jakichś poufnych danych z historii czatu.

[21] NORM lesson=L02 stated=347-348 found=347 kind=capability
     ITEM: Employ the Sampling feature when the server needs an AI to make decisions, such as classifying data, before returning a result.
     QUOTE: Użyj tego, kiedy na przykład serwer musi podjąć jakieś decyzje typu sklasyfikowanie jakichś danych przed zwróceniem ich.

[22] NORM lesson=L02 stated=398-401 found=398 kind=architecture
     ITEM: Base your design only on primitives that your target clients actually support to avoid deploying a server that is unusable for certain users.
     QUOTE: upewnić się, że opierasz się o te konkretne prymitywy, które funkcjonują w Twoich klientach, żeby nie odciąć części użytkowników albo nie spowodować, że wdrożysz serwer, który dla części użytkowników będzie całkowicie niestrawny.

[23] NORM lesson=L02 stated=416-418 found=416 kind=architecture
     ITEM: Use SSE for remote communication when the server primarily needs to push proactive updates to the client.
     QUOTE: Mamy dostępne SSE i to powinniśmy wykorzystać, kiedy serwer głównie wysyła aktualizacje do klienta, bo potrzebuje aktualizacji, o której MCP Client pasywnie nie pyta

[24] NORM lesson=L02 stated=434-437 found=433 kind=architecture
     ITEM: Select Stateless mode only for simple tools that do not involve complex server-side logic or long-running operations requiring notifications.
     QUOTE: tryb Stateless powinniśmy wybrać tylko wtedy, kiedy nasze narzędzia są proste, nie wymagają jakiegoś myślenia po stronie serwera czy długotrwałych operacji z powiadomieniami.

[25] NORM lesson=L02 stated=439-441 found=439 kind=architecture
     ITEM: Utilize JSON Response Mode when you only require standard JSON responses and do not need streaming capabilities.
     QUOTE: Jeżeli nie potrzebujemy streamingu, czyli potrzebujemy czystego JSON-a, możemy użyć JSON Response Mode.

[26] NORM lesson=L02 stated=448-449 found=448 kind=architecture
     ITEM: Choose the stdio transport method when establishing local communication between processes.
     QUOTE: jeżeli chcesz pracować lokalnie, no to oczywiście używasz stdio.

[27] EXACT lesson=L02 stated=449 found=449 kind=architecture
     ITEM: Implement Streamable HTTP for remote integrations with SaaS platforms.
     QUOTE: Jeżeli pracujesz zdalnie z jakimś SaaS-em, używasz Streamable HTTP.

[28] NORM lesson=L02 stated=450-452 found=450 kind=architecture
     ITEM: Ensure Session Affinity is configured in your infrastructure when using Stateful mode for advanced features like Sampling, subscriptions, or Progress Tracking.
     QUOTE: jeżeli potrzebujesz pełnej mocy, czyli Sampling, subskrypcji, Progress Tracking i tak dalej, to wybierasz tryb Stateful i musisz wtedy zapewnić Session Affinity, czyli stickiness na swojej infrastrukturze.

[29] NORM lesson=L02 stated=452-454 found=452 kind=architecture
     ITEM: Select Stateless mode to prioritize horizontal scaling and simplicity, accepting the lack of advanced interactive features.
     QUOTE: Jeżeli priorytetem jest skalowanie horyzontalne, prostota, wybierasz tryb Stateless i akceptujesz brak tych zaawansowanych funkcji interaktywnych.

[30] NORM lesson=L03 stated=494-495 found=495 kind=obligation
     ITEM: Include a WWW-Authenticate header containing the resource_metadata URL when returning a 401 Unauthorized response.
     QUOTE: ten 401 musi zawierać header WWW-Authenticate z URL-em do resource_metadata.

[31] NORM lesson=L03 stated=539-540 found=539 kind=security
     ITEM: Verify that the presented OAuth token was issued specifically for your server by implementing Audience Binding.
     QUOTE: MCP Server powinien sprawdzić, czy token został wystawiony dokładnie dla tego serwera.

[32] NORM lesson=L03 stated=543-546 found=543 kind=security
     ITEM: Issue short-lived access tokens so their validity and user consent are frequently re-checked during the refresh token rotation.
     QUOTE: ten access token powinien żyć w miarę krótko po to, żeby na poziomie regeneracji refresh tokena moglibyśmy sprawdzić, czy ten token przynajmniej nie został zinwalidowany albo czy użytkownik już nie wycofał tego poświadczenia.

[33] NORM lesson=L03 stated=552-554 found=552 kind=security
     ITEM: Always enforce the use of PKCE with the S256 algorithm to maintain security standards.
     QUOTE: PKCE z obowiązkowym S256 jest niezmiennie wymaganym algorytmem do zapewnienia bezpieczeństwa.

[34] NORM lesson=L03 stated=563-565 found=563 kind=security
     ITEM: Validate the state parameter and strictly bind the user's browser session to the initiated login process to prevent session hijacking.
     QUOTE: Nie było bindowania stanu czy weryfikowania parametru state, i sesja użytkownika w przeglądarce nie była sztywnie powiązana z zainicjowanym procesem logowania.

[35] NORM lesson=L03 stated=595-598 found=595 kind=security
     ITEM: Apply the principle of least privilege by generating highly granular permissions per resource or repository to limit the blast radius.
     QUOTE: stosując minimalizację uprawnień, generować bardzo granularne uprawnienia do poszczególnego jednego zasobu, do poszczególnego repozytorium, po to, żeby ograniczać tak zwany Blast Radius.

[36] NORM lesson=L03 stated=599-601 found=599 kind=security
     ITEM: Implement supplementary permissions specifically for reading personal data to prevent its accidental exposure to the model.
     QUOTE: Można na przykład wprowadzać dodatkowe uprawnienia do odczytywania danych osobowych, po to, żeby dodatkowo chronić je przed przypadkowym wyciekiem do modelu.

[37] NORM lesson=L03 stated=611-613 found=611 kind=security
     ITEM: Verify the JWT signature on the server for each request to ensure it originates from the private key owner under the Demonstrated Proof of Possession mechanism.
     QUOTE: przy każdym żądaniu MCP Client będzie musiał wygenerować i podpisać ten obiekt JWT, po to, żeby serwer mógł sprawdzić podpis i upewnić się, że żądanie pochodzi od właściciela klucza prywatnego

[38] NORM lesson=L04 stated=646-648 found=646 kind=practice
     ITEM: Develop your MCP Server using the transport mechanism that you intend to use in production because there are fundamental differences between transports.
     QUOTE: Pierwsza rzecz jest taka, że zwracaj bardzo uwagę na to, żeby rozwijać swój MCP Server w tym rodzaju transportu, który będziesz wykorzystywał produkcyjnie, ponieważ pomiędzy tymi różnymi transportami jest sporo zasadniczych różnic.

[39] NORM lesson=L04 stated=652-654 found=652 kind=capability
     ITEM: You must open an SSE channel when using HTTP transport if you want the server to be able to query the model for context, as HTTP is otherwise unidirectional.
     QUOTE: W przypadku transportu HTTP serwer tylko odpowiada, bez otwarcia kanału SSE, nie ma możliwości, nie ma mowy o dopytywaniu modelu o jakiś konkretny kontekst.

[40] NORM lesson=L04 stated=662-665 found=662 kind=lifecycle
     ITEM: Ensure that your load balancer does not prematurely terminate SSE sessions when using HTTP transport, because MCP needs a stable and long data stream to function correctly.
     QUOTE: W przypadku HTTP tam mamy sieciowy cykl i tutaj musimy się na przykład upewnić, że load balancer nie przerywa sesji SSE zbyt wcześnie, bo MCP wymaga stabilnego i długiego strumienia danych do tego, żeby poprawnie funkcjonować.

[41] NORM lesson=L04 stated=691-695 found=691 kind=observability
     ITEM: Inspect security events at your edge or WAF for rules that block specific user agents if you encounter unexpected connection failures, or bypass the WAF to verify if it is the source of the issue.
     QUOTE: Jeżeli będziecie mieć jakiekolwiek takie dziwne zachowanie, gdzie coś Wam się wydaje, że powinno działać, a nagle nie działa, sprawdźcie zdarzenia bezpieczeństwa na poziomie Waszego edge'a czy WAF-a. Czy nie ma jakichś reguł, które blokują konkretnych user agentów? Albo zróbcie na przykład bypass na WAF-ie, żeby potwierdzić, że to jest źródłem problemu.

[42] NORM lesson=L04 stated=702-706 found=702 kind=anti-pattern
     ITEM: Avoid declaring a massive number of tools on a single MCP Server to prevent exhausting the context window with tool schemas during initialization.
     QUOTE: mamy część narzędzi czy MCP Server, które deklarują bardzo dużą liczbę narzędzi, na przykład 50 czy 100 narzędzi. Każdy z tych narzędzi ma swój opis, ma opis struktury wejściowej i wyjściowej, i efekt jest taki, że taki jeden MCP Server potrafi zjeść kilkadziesiąt tysięcy tokenów na starcie serwera.

[43] NORM lesson=L04 stated=717-719 found=717 kind=obligation
     ITEM: You must ensure perfect alignment between the schema definition and the returned JSON, as any discrepancy will immediately abort the tool execution and return an error.
     QUOTE: Jeżeli będzie jakiś najmniejszy rozjazd pomiędzy definicją schematu a tym, co wraca w JSON-ie, jest natychmiast przerywane wywołanie narzędzia i jest zgłaszany błąd.

[44] NORM lesson=L04 stated=721-723 found=721 kind=practice
     ITEM: Implement a cancel mechanism for long-running operations to avoid permanently blocking the chat thread until the connection drops.
     QUOTE: Tak samo, jeżeli nie zaimplementujecie cancel przy długich operacjach, może to zablokować cały wątek czatu tak długo, jak czat nie stwierdzi, że trzeba uwalić dane połączenie, bo no nic dobrego już nie przyniesie.

[45] NORM lesson=L04 stated=740-742 found=740 kind=versioning
     ITEM: Version your tools by introducing new method names instead of applying breaking changes to existing contracts.
     QUOTE: Pierwsze to jest wersjonowanie, czyli tak naprawdę wersjonujemy narzędzie wewnątrz serwera, czyli tworzymy na przykład metodę ge_user_v2 zamiast zmieniać w sposób łamiący kontrakt metody getUser.

[46] NORM lesson=L04 stated=747-749 found=747 kind=lifecycle
     ITEM: Send a notifications/tools/list_changed notification so the MCP Client reloads the tool list and definitions when changes occur.
     QUOTE: Druga rzecz to są notyfikacje, czyli możliwość wysłania notyfikacji notifications/tools/list_changed, po którym MCP Client powinien przeładować listę narzędzi razem z definicją tych narzędzi.

[47] NORM lesson=L04 stated=774-776 found=774 kind=architecture
     ITEM: Expose additional methods or tools that return a list of available filtering criteria specific to a user's permissions to handle dynamic constraints.
     QUOTE: Teraz to, co możemy zrobić, to my na przykład tworzymy dodatkowe metody czy dodatkowe narzędzia, które zwracają na przykład list available criterias, czyli zwracają listę dodatkowych filtrów, po których dany użytkownik może szukać.

[48] NORM lesson=L04 stated=824-827 found=824 kind=architecture
     ITEM: Integrate your MCP Server with internal bots or internal application features rather than exposing it publicly for general business consumers.
     QUOTE: W przypadku biznesowym nie myśl o publikacji i publicznym wystawieniu narzędzia MCP Server, ale o zapięciu MCP Server do wewnętrznych botów i do wewnętrznych funkcji udostępnionych w ramach Twojej aplikacji.

[49] NORM lesson=L05 stated=848-850 found=847 kind=obligation
     ITEM: You must implement MCP as a stateless, unidirectional request-response protocol because the stateful mode was removed in the new specification.
     QUOTE: Ta specyfikacja mówi natomiast, że jego trzeba używać w trybie stateless, bo ten tryb stanowy został usunięty. Czyli MCP z takiego dwukierunkowego, stanowego protokołu staje się jednokierunkowym protokołem request response.

[50] NORM lesson=L05 stated=850-851 found=850 kind=versioning
     ITEM: Note that initialization, MCP session notifications, and ping have been removed and can no longer be used.
     QUOTE: To znaczy, że cała inicjalizacja, notyfikacje MCP session i ping zostały usunięte i nie kuszą już do stosowania tej technologii.

[51] NORM lesson=L05 stated=856-858 found=856 kind=architecture
     ITEM: Your server must integrate directly with an LLM via its own API to communicate with it, as sampling has been deprecated.
     QUOTE: Czyli teraz, jeżeli nasz serwer potrzebuje porozmawiać z modelem LLM, musi po prostu użyć swojego API i bezpośrednio z tym modelem się zintegrować.

[52] NORM lesson=L05 stated=860-861 found=860 kind=versioning
     ITEM: Pass entire paths exclusively as a URI tool parameter, because the separate roots technology has been eliminated.
     QUOTE: Nie mamy także technologii roots. Teraz ścieżki są przekazywane po prostu jako parametr narzędzia URI w całości.

[53] NORM lesson=L05 stated=861-863 found=861 kind=observability
     ITEM: Use OpenTelemetry for robust logging, or standard stderr in stdio, as native protocol logging has been removed.
     QUOTE: Nie ma logowania. Jeżeli potrzebujemy logować to w stdio okej, możemy sobie wbić na stderr, natomiast taką preferowaną technologią jest po prostu użycie OpenTelemetry.

[54] NORM lesson=L05 stated=863-865 found=863 kind=versioning
     ITEM: You cannot use HTTP plus SSE transport as that separate stream was removed; rely instead on streamable HTTP.
     QUOTE: Nie ma też w tej chwili transportu HTTP plus SSE. Ten osobny strumień SSE został usunięty. Dalej mamy streamable HTTP, natomiast na tym się kończy.

[55] NORM lesson=L05 stated=865-869 found=865 kind=versioning
     ITEM: Use Client ID Metadata Documents, which have completely replaced dynamic client registration.
     QUOTE: Nie mamy też patologicznego dynamic client registration, który jeszcze niedawno był wymuszany przez dostawców takich jak Anthropic i OpenID i nie dało się tak naprawdę podpiąć swojego serwera MCP pod nich, jeżeli tego dynamic client registration nie stosowaliśmy. W tej chwili to zostało zamienione przez Client ID Metadata Documents.

[56] NORM lesson=L05 stated=876-879 found=876 kind=anti-pattern
     ITEM: Do not design new MCP servers using deprecated stateful features, as they will require a complete rewrite when the transition period ends.
     QUOTE: Natomiast warto tak naprawdę już o tym wiedzieć i nie projektować serwerów MCP, wykorzystujących te zdeprecjonowane technologie, bo będzie to znaczyło konieczność ich całkowitej przebudowy.

[57] NORM lesson=L05 stated=881-884 found=881 kind=obligation
     ITEM: You must pass the protocol version, identity, and capabilities inside the meta parameter with every single request, rather than just at initialization.
     QUOTE: Przede wszystkim każdy request w tej chwili musi opisywać sam siebie. Czyli wersja protokołu, tożsamość, capabilities, które w tej chwili były przy inicjalizacji, one za każdym razem muszą być przekazywane w parametrze meta.

[58] NORM lesson=L05 stated=887-889 found=887 kind=obligation
     ITEM: Your server must implement the new server discover method to allow clients to negotiate supported capability versions.
     QUOTE: Pojawiła się nowa metoda server discover, którą serwer musi implementować, natomiast klient może ją wywołać, żeby poznać właśnie wspierane wersje capabilities i tak naprawdę uprościć pracę z tym i negocjowanie wersji, którą mamy.

[59] NORM lesson=L05 stated=895-898 found=895 kind=capability
     ITEM: You can allow the client to cache responses for endpoints like tools/list, prompts/list, resources/list, or resources/read.
     QUOTE: I tutaj z pomocą przychodzi nam cache, który mówi, że dla takich metod jak tools/list, prompts/list, resources/list czy resources/read tak naprawdę mamy możliwość zapisania po stronie klienta w cache'u odpowiedzi.

[60] NORM lesson=L05 stated=900-901 found=900 kind=obligation
     ITEM: You must define whether a cache is global or user-specific by returning the cacheScope parameter in the response.
     QUOTE: To sobie określamy tak naprawdę w odpowiedzi na to takim parametrem cacheScope, który mówi, czy to jest global, czy jest user.

[61] NORM lesson=L05 stated=902-903 found=902 kind=obligation
     ITEM: You must provide a TTL parameter in milliseconds in the response to define how long the client is allowed to retain the cached data.
     QUOTE: Dodatkowym parametrem jest TTL w milisekundach, który mówi, jak długo klient może tą odpowiedź zatrzymać.

[62] NORM lesson=L05 stated=915-917 found=915 kind=capability
     ITEM: Return a resultType of input_required and a list of missing parameters from the server to prompt the client for more information.
     QUOTE: serwer tak naprawdę nie może dopytać klienta, natomiast może w odpowiedzi zwrócić resultType pod tytułem input_required i uwzględnić tam listę brakują parametrów

[63] NORM lesson=L05 stated=921-923 found=921 kind=obligation
     ITEM: The client must prompt its user for any missing parameters and resend the initial request augmented with an input_responses field containing the user's answers.
     QUOTE: I teraz klient, który otrzymał to dopyta swojego użytkownika o te parametry, po czym to inicjalne wywołanie, które poszło z zamówieniem, wzbogacone o pole input_responses, które zawiera odpowiedzi na te pytania, wyśle do serwera.

[64] NORM lesson=L05 stated=937-939 found=937 kind=architecture
     ITEM: You can manage state based directly on the logged-in user if your application's logic permits tying a resource strictly to that user's identity.
     QUOTE: Jeżeli logika naszej aplikacji działa w ten sposób, że mamy, nie wiem, na przykład jeden koszyk tylko dostępny dla użytkownika, to wtedy tak naprawdę na podstawie zalogowanego użytkownika możemy ten stan obsługiwać.

[65] NORM lesson=L05 stated=943-945 found=943 kind=architecture
     ITEM: You must maintain state by continuously passing a designated state-tracking parameter between the client and the server if user-based authorization isn't sufficient.
     QUOTE: Natomiast jeżeli takiej logiki nie mamy, to musimy oprzeć się tak naprawdę o parametr, który będzie przekazywany cały czas pomiędzy klientem a serwerem.

[66] NORM lesson=L05 stated=949-952 found=949 kind=naming
     ITEM: Provide explicit names and descriptions for state parameters so the model understands exactly how to handle them.
     QUOTE: Tutaj warto zadbać o odpowiednie nazewnictwo i opis tych parametrów, żeby model nie miał wątpliwości, w jaki sposób z tym możemy pracować, tak?

[67] NORM lesson=L05 stated=1014-1017 found=1014 kind=obligation
     ITEM: The server must declare its support for the Enterprise Managed Authorization extension at the OAuth Protected Resources level.
     QUOTE: Ważne jest to, że serwer deklaruje już na poziomie OAuth Protected Resources informację o tym, że wspiera to extension, a klient znowu w meta może wysłać, że to ma.

[68] NORM lesson=L05 stated=1021-1022 found=1021 kind=practice
     ITEM: Implement the Enterprise Managed Authorization extension immediately instead of waiting for the new Multi Round-Trip Requests SDK.
     QUOTE: I o ile z wejściem w ten MRTR to musimy jeszcze zaczekać, aż to SDK faktycznie się pojawi, to jest coś, z czym bym nie czekał i wszedłbym w to jak tylko się da najszybciej.

[69] NORM lesson=L06 stated=1038-1040 found=1038 kind=capability
     ITEM: Define your server capabilities, such as Tools, Prompts, and Resources.
     QUOTE: mamy tutaj tak naprawdę możliwość zdefiniowania. Po pierwsze, jakie capabilities będzie zawierał nasz serwer, czyli mamy Tools, mamy Prompts, mamy Resources.

[70] NORM lesson=L06 stated=1053-1055 found=1054 kind=obligation
     ITEM: Describe tool schemas accurately so that the LLM knows what information to expect.
     QUOTE: Tak naprawdę musi być bardzo dokładnie opisane, żeby LLM wiedział, jakich informacji się spodziewać.

[71] NORM lesson=L06 stated=1065-1067 found=1065 kind=architecture
     ITEM: Expose a controller that returns /.well-known/ metadata, such as the resource, Authorization Server, and supported scopes.
     QUOTE: Dodatkowo mamy kontroler, który zwraca nam te informacje /.well-known/, takie jak resource, Authorization Server, scope'y, jakie są wspierane i tak dalej.

[72] NORM lesson=L06 stated=1094-1095 found=1094 kind=obligation
     ITEM: Return a 401 status code for unauthenticated requests, in accordance with the specification.
     QUOTE: Możemy wejść na ten URL i zobaczymy, że tutaj dostaniemy 401, czyli tak jak powinno być zgodnie ze specyfikacją.

[73] NORM lesson=L06 stated=1099-1101 found=1099 kind=practice
     ITEM: Return a 401 response with a header that indicates the location of all metadata when a request fails authentication.
     QUOTE: mamy POST'a do mojego MCP Server, który zwraca 401 razem z tym headerem, który mówi: no niestety nie udało się, ale tutaj masz informację o tym, gdzie są wszystkie metadane.

[74] NORM lesson=L06 stated=1120-1124 found=1120 kind=observability
     ITEM: Be aware that requests from the LLM to the MCP server might be blocked by WAFs as malicious bot traffic.
     QUOTE: jeżeli po wykonaniu tego żądania nie widzielibyście dalej odwołań do MCP, one prawdopodobnie są blokowane jako złośliwy ruch, ponieważ Cloudflare i inne WAF-y potrafią wycinać cały ruch, który idzie od Claude'a. Tutaj to jeszcze nie jest wykrywane jako ruch botów, natomiast to, co idzie do MCP, idzie bezpośrednio z LLM-a i to już jest wykrywane jako ruch bota.

[75] NORM lesson=L06 stated=1156-1157 found=1156 kind=anti-pattern
     ITEM: Avoid passing the token directly from the MCP client to the server.
     QUOTE: W trakcie naszego wykładu wcześniejszego mówiliśmy o tym, że przekazywanie tokena z MCP bezpośrednio do serwera nie jest najlepszym pomysłem.

[76] NORM lesson=L07 stated=1183-1184 found=1182 kind=security
     ITEM: Handle authorization in the MCP server without directly passing tokens.
     QUOTE: w jaki sposób nasz MCP Server powinien obsługiwać autoryzację bez przekazywania tokenów.

[77] NORM lesson=L07 stated=1195-1196 found=1195 kind=architecture
     ITEM: Implement a Token Introspection mechanism to check incoming tokens.
     QUOTE: Zaimplementujemy mechanizm Token Introspection, który ma sprawdzać te tokeny przychodzące

[78] NORM lesson=L07 stated=1196-1198 found=1196 kind=architecture
     ITEM: Implement a Token Exchange mechanism to fetch a backend-specific token based on the token obtained from the MCP.
     QUOTE: i Token Exchange, który pozwoli nam pobrać na podstawie tego tokena uzyskanego z MCP bezpośrednio token dla usług backendowych.

[79] NORM lesson=L07 stated=1217-1218 found=1217 kind=practice
     ITEM: Implement a field or filter in the MCP Server that performs introspection on the token received directly from the MCP Server.
     QUOTE: mamy tutaj zaimplementowany field, który robi introspekcję tego tokena, który przychodzi z MCP Server bezpośrednio

[80] NORM lesson=L07 stated=1218-1220 found=1218 kind=practice
     ITEM: Use a TokenExchangeClient to exchange the initial token for a new one after successful introspection.
     QUOTE: i jeżeli to jest ok, to tak naprawdę po zawołaniu tej introspekcji mamy TokenExchangeClient, który robi exchange tokenów i strzela po wymianę tego jednego tokena na drugi

[81] NORM lesson=L07 stated=1220-1221 found=1220 kind=obligation
     ITEM: Pass the exchanged token to the backend instead of the original one.
     QUOTE: i dalej wszystko idzie już tak samo, czyli też ten konkretny token wymieniony będzie przekazywany do backendu.

[82] NORM lesson=L07 stated=1223-1225 found=1223 kind=architecture
     ITEM: Implement an IntrospectionFilter on the backend side to introspect the exchanged token it receives.
     QUOTE: Jeżeli chodzi o backend, też możemy sobie tutaj zobaczyć w kontekście OAuth, że mamy na przykład IntrospectionFilter, który robi nam introspekcję tego tokenu
