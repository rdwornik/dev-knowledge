Consumers: `[#765]` (the row this evidence serves), `[#696]` (the locator defect it answers)

# agy leg -- prompt_l2.txt
# model: gemini-3.1-pro-high
# invocation: agy --model gemini-3.1-pro-high --output-format json --print-timeout 20m --dangerously-skip-permissions --print=<prompt_l2.txt>
# exit: 0 | wall: 134.0s | status: SUCCESS | usage: {'input_tokens': 17275, 'output_tokens': 23886, 'thinking_tokens': 20608, 'cache_read_tokens': 20287, 'total_tokens': 41161}
# ordered reader, not substituted

ITEM: Develop your MCP Server using the transport mechanism that you intend to use in production because there are fundamental differences between transports.
LESSON: L04
LINES: 646-648
QUOTE: Pierwsza rzecz jest taka, że zwracaj bardzo uwagę na to, żeby rozwijać swój MCP Server w tym rodzaju transportu, który będziesz wykorzystywał produkcyjnie, ponieważ pomiędzy tymi różnymi transportami jest sporo zasadniczych różnic.
KIND: practice

ITEM: You must open an SSE channel when using HTTP transport if you want the server to be able to query the model for context, as HTTP is otherwise unidirectional.
LESSON: L04
LINES: 652-654
QUOTE: W przypadku transportu HTTP serwer tylko odpowiada, bez otwarcia kanału SSE, nie ma możliwości, nie ma mowy o dopytywaniu modelu o jakiś konkretny kontekst.
KIND: capability

ITEM: Ensure that your load balancer does not prematurely terminate SSE sessions when using HTTP transport, because MCP needs a stable and long data stream to function correctly.
LESSON: L04
LINES: 662-665
QUOTE: W przypadku HTTP tam mamy sieciowy cykl i tutaj musimy się na przykład upewnić, że load balancer nie przerywa sesji SSE zbyt wcześnie, bo MCP wymaga stabilnego i długiego strumienia danych do tego, żeby poprawnie funkcjonować.
KIND: lifecycle

ITEM: Inspect security events at your edge or WAF for rules that block specific user agents if you encounter unexpected connection failures, or bypass the WAF to verify if it is the source of the issue.
LESSON: L04
LINES: 691-695
QUOTE: Jeżeli będziecie mieć jakiekolwiek takie dziwne zachowanie, gdzie coś Wam się wydaje, że powinno działać, a nagle nie działa, sprawdźcie zdarzenia bezpieczeństwa na poziomie Waszego edge'a czy WAF-a. Czy nie ma jakichś reguł, które blokują konkretnych user agentów? Albo zróbcie na przykład bypass na WAF-ie, żeby potwierdzić, że to jest źródłem problemu.
KIND: observability

ITEM: Avoid declaring a massive number of tools on a single MCP Server to prevent exhausting the context window with tool schemas during initialization.
LESSON: L04
LINES: 702-706
QUOTE: mamy część narzędzi czy MCP Server, które deklarują bardzo dużą liczbę narzędzi, na przykład 50 czy 100 narzędzi. Każdy z tych narzędzi ma swój opis, ma opis struktury wejściowej i wyjściowej, i efekt jest taki, że taki jeden MCP Server potrafi zjeść kilkadziesiąt tysięcy tokenów na starcie serwera.
KIND: anti-pattern

ITEM: You must ensure perfect alignment between the schema definition and the returned JSON, as any discrepancy will immediately abort the tool execution and return an error.
LESSON: L04
LINES: 717-719
QUOTE: Jeżeli będzie jakiś najmniejszy rozjazd pomiędzy definicją schematu a tym, co wraca w JSON-ie, jest natychmiast przerywane wywołanie narzędzia i jest zgłaszany błąd.
KIND: obligation

ITEM: Implement a cancel mechanism for long-running operations to avoid permanently blocking the chat thread until the connection drops.
LESSON: L04
LINES: 721-723
QUOTE: Tak samo, jeżeli nie zaimplementujecie cancel przy długich operacjach, może to zablokować cały wątek czatu tak długo, jak czat nie stwierdzi, że trzeba uwalić dane połączenie, bo no nic dobrego już nie przyniesie.
KIND: practice

ITEM: Version your tools by introducing new method names instead of applying breaking changes to existing contracts.
LESSON: L04
LINES: 740-742
QUOTE: Pierwsze to jest wersjonowanie, czyli tak naprawdę wersjonujemy narzędzie wewnątrz serwera, czyli tworzymy na przykład metodę ge_user_v2 zamiast zmieniać w sposób łamiący kontrakt metody getUser.
KIND: versioning

ITEM: Send a notifications/tools/list_changed notification so the MCP Client reloads the tool list and definitions when changes occur.
LESSON: L04
LINES: 747-749
QUOTE: Druga rzecz to są notyfikacje, czyli możliwość wysłania notyfikacji notifications/tools/list_changed, po którym MCP Client powinien przeładować listę narzędzi razem z definicją tych narzędzi.
KIND: lifecycle

ITEM: Expose additional methods or tools that return a list of available filtering criteria specific to a user's permissions to handle dynamic constraints.
LESSON: L04
LINES: 774-776
QUOTE: Teraz to, co możemy zrobić, to my na przykład tworzymy dodatkowe metody czy dodatkowe narzędzia, które zwracają na przykład list available criterias, czyli zwracają listę dodatkowych filtrów, po których dany użytkownik może szukać.
KIND: architecture

ITEM: Integrate your MCP Server with internal bots or internal application features rather than exposing it publicly for general business consumers.
LESSON: L04
LINES: 824-827
QUOTE: W przypadku biznesowym nie myśl o publikacji i publicznym wystawieniu narzędzia MCP Server, ale o zapięciu MCP Server do wewnętrznych botów i do wewnętrznych funkcji udostępnionych w ramach Twojej aplikacji.
KIND: architecture

ITEM: You must implement MCP as a stateless, unidirectional request-response protocol because the stateful mode was removed in the new specification.
LESSON: L05
LINES: 848-850
QUOTE: Ta specyfikacja mówi natomiast, że jego trzeba używać w trybie stateless, bo ten tryb stanowy został usunięty. Czyli MCP z takiego dwukierunkowego, stanowego protokołu staje się jednokierunkowym protokołem request response.
KIND: obligation

ITEM: Note that initialization, MCP session notifications, and ping have been removed and can no longer be used.
LESSON: L05
LINES: 850-851
QUOTE: To znaczy, że cała inicjalizacja, notyfikacje MCP session i ping zostały usunięte i nie kuszą już do stosowania tej technologii.
KIND: versioning

ITEM: Your server must integrate directly with an LLM via its own API to communicate with it, as sampling has been deprecated.
LESSON: L05
LINES: 856-858
QUOTE: Czyli teraz, jeżeli nasz serwer potrzebuje porozmawiać z modelem LLM, musi po prostu użyć swojego API i bezpośrednio z tym modelem się zintegrować.
KIND: architecture

ITEM: Pass entire paths exclusively as a URI tool parameter, because the separate roots technology has been eliminated.
LESSON: L05
LINES: 860-861
QUOTE: Nie mamy także technologii roots. Teraz ścieżki są przekazywane po prostu jako parametr narzędzia URI w całości.
KIND: versioning

ITEM: Use OpenTelemetry for robust logging, or standard stderr in stdio, as native protocol logging has been removed.
LESSON: L05
LINES: 861-863
QUOTE: Nie ma logowania. Jeżeli potrzebujemy logować to w stdio okej, możemy sobie wbić na stderr, natomiast taką preferowaną technologią jest po prostu użycie OpenTelemetry.
KIND: observability

ITEM: You cannot use HTTP plus SSE transport as that separate stream was removed; rely instead on streamable HTTP.
LESSON: L05
LINES: 863-865
QUOTE: Nie ma też w tej chwili transportu HTTP plus SSE. Ten osobny strumień SSE został usunięty. Dalej mamy streamable HTTP, natomiast na tym się kończy.
KIND: versioning

ITEM: Use Client ID Metadata Documents, which have completely replaced dynamic client registration.
LESSON: L05
LINES: 865-869
QUOTE: Nie mamy też patologicznego dynamic client registration, który jeszcze niedawno był wymuszany przez dostawców takich jak Anthropic i OpenID i nie dało się tak naprawdę podpiąć swojego serwera MCP pod nich, jeżeli tego dynamic client registration nie stosowaliśmy. W tej chwili to zostało zamienione przez Client ID Metadata Documents.
KIND: versioning

ITEM: Do not design new MCP servers using deprecated stateful features, as they will require a complete rewrite when the transition period ends.
LESSON: L05
LINES: 876-879
QUOTE: Natomiast warto tak naprawdę już o tym wiedzieć i nie projektować serwerów MCP, wykorzystujących te zdeprecjonowane technologie, bo będzie to znaczyło konieczność ich całkowitej przebudowy.
KIND: anti-pattern

ITEM: You must pass the protocol version, identity, and capabilities inside the meta parameter with every single request, rather than just at initialization.
LESSON: L05
LINES: 881-884
QUOTE: Przede wszystkim każdy request w tej chwili musi opisywać sam siebie. Czyli wersja protokołu, tożsamość, capabilities, które w tej chwili były przy inicjalizacji, one za każdym razem muszą być przekazywane w parametrze meta.
KIND: obligation

ITEM: Your server must implement the new server discover method to allow clients to negotiate supported capability versions.
LESSON: L05
LINES: 887-889
QUOTE: Pojawiła się nowa metoda server discover, którą serwer musi implementować, natomiast klient może ją wywołać, żeby poznać właśnie wspierane wersje capabilities i tak naprawdę uprościć pracę z tym i negocjowanie wersji, którą mamy.
KIND: obligation

ITEM: You can allow the client to cache responses for endpoints like tools/list, prompts/list, resources/list, or resources/read.
LESSON: L05
LINES: 895-898
QUOTE: I tutaj z pomocą przychodzi nam cache, który mówi, że dla takich metod jak tools/list, prompts/list, resources/list czy resources/read tak naprawdę mamy możliwość zapisania po stronie klienta w cache'u odpowiedzi.
KIND: capability

ITEM: You must define whether a cache is global or user-specific by returning the cacheScope parameter in the response.
LESSON: L05
LINES: 900-901
QUOTE: To sobie określamy tak naprawdę w odpowiedzi na to takim parametrem cacheScope, który mówi, czy to jest global, czy jest user.
KIND: obligation

ITEM: You must provide a TTL parameter in milliseconds in the response to define how long the client is allowed to retain the cached data.
LESSON: L05
LINES: 902-903
QUOTE: Dodatkowym parametrem jest TTL w milisekundach, który mówi, jak długo klient może tą odpowiedź zatrzymać.
KIND: obligation

ITEM: Return a resultType of input_required and a list of missing parameters from the server to prompt the client for more information.
LESSON: L05
LINES: 915-917
QUOTE: serwer tak naprawdę nie może dopytać klienta, natomiast może w odpowiedzi zwrócić resultType pod tytułem input_required i uwzględnić tam listę brakują parametrów
KIND: capability

ITEM: The client must prompt its user for any missing parameters and resend the initial request augmented with an input_responses field containing the user's answers.
LESSON: L05
LINES: 921-923
QUOTE: I teraz klient, który otrzymał to dopyta swojego użytkownika o te parametry, po czym to inicjalne wywołanie, które poszło z zamówieniem, wzbogacone o pole input_responses, które zawiera odpowiedzi na te pytania, wyśle do serwera.
KIND: obligation

ITEM: You can manage state based directly on the logged-in user if your application's logic permits tying a resource strictly to that user's identity.
LESSON: L05
LINES: 937-939
QUOTE: Jeżeli logika naszej aplikacji działa w ten sposób, że mamy, nie wiem, na przykład jeden koszyk tylko dostępny dla użytkownika, to wtedy tak naprawdę na podstawie zalogowanego użytkownika możemy ten stan obsługiwać.
KIND: architecture

ITEM: You must maintain state by continuously passing a designated state-tracking parameter between the client and the server if user-based authorization isn't sufficient.
LESSON: L05
LINES: 943-945
QUOTE: Natomiast jeżeli takiej logiki nie mamy, to musimy oprzeć się tak naprawdę o parametr, który będzie przekazywany cały czas pomiędzy klientem a serwerem.
KIND: architecture

ITEM: Provide explicit names and descriptions for state parameters so the model understands exactly how to handle them.
LESSON: L05
LINES: 949-952
QUOTE: Tutaj warto zadbać o odpowiednie nazewnictwo i opis tych parametrów, żeby model nie miał wątpliwości, w jaki sposób z tym możemy pracować, tak?
KIND: naming

ITEM: The server must declare its support for the Enterprise Managed Authorization extension at the OAuth Protected Resources level.
LESSON: L05
LINES: 1014-1017
QUOTE: Ważne jest to, że serwer deklaruje już na poziomie OAuth Protected Resources informację o tym, że wspiera to extension, a klient znowu w meta może wysłać, że to ma.
KIND: obligation

ITEM: Implement the Enterprise Managed Authorization extension immediately instead of waiting for the new Multi Round-Trip Requests SDK.
LESSON: L05
LINES: 1021-1022
QUOTE: I o ile z wejściem w ten MRTR to musimy jeszcze zaczekać, aż to SDK faktycznie się pojawi, to jest coś, z czym bym nie czekał i wszedłbym w to jak tylko się da najszybciej.
KIND: practice
