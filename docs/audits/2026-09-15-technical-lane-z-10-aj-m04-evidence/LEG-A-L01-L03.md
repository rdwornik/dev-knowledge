Consumers: `[#784]` (the row this evidence serves), `[#696]` (the locator defect it answers)

# agy leg -- prompt_l1.txt
# model: gemini-3.1-pro-high
# invocation: agy --model gemini-3.1-pro-high --output-format json --print-timeout 20m --dangerously-skip-permissions --print=<prompt_l1.txt>
# exit: 0 | wall: 132.7s | status: SUCCESS | usage: {'input_tokens': 30335, 'output_tokens': 22801, 'thinking_tokens': 19467, 'cache_read_tokens': 12210, 'total_tokens': 53136}
# ordered reader, not substituted

ITEM: Maintain an architectural separation of concerns where MCP defines the tool request format while the application independently manages the model and tool invocation logic.
LESSON: L01
LINES: 17-19
QUOTE: MCP definiuje format danych, czyli to, jak model ma prosić narzędzia, ale nie narzuca aplikacji, jak ma zarządzać modelem albo jak agent i kiedy powinien wywoływać dane narzędzia.
KIND: architecture

ITEM: Implement connection management, user consent prompts, and authorization flows when building an enterprise chatbot that acts as an MCP Host.
LESSON: L01
LINES: 59-61
QUOTE: Czyli to Wy będziecie musieli zaimplementować i zdecydować, jak zarządzać wieloma połączeniami, jak pytać użytkowników o zgodę, jak zarządzać autoryzacją.
KIND: architecture

ITEM: Re-establish the connection with a new handshake if you need to use capabilities that were not declared initially.
LESSON: L01
LINES: 111-112
QUOTE: nie ma możliwości, żeby zacząć obsługiwać te obrazki bez nawiązania ponownego połączenia, czyli bez ponownego Handshake'u.
KIND: lifecycle

ITEM: Adhere strictly to the capabilities and versions negotiated during the initial handshake, as they remain fixed for the entire duration of the session.
LESSON: L01
LINES: 112-113
QUOTE: To, co zostanie wynegocjowane tutaj, jest wiążące przez całą sesję.
KIND: lifecycle

ITEM: Provide descriptions for both the tool itself and its input/output schema when defining it.
LESSON: L02
LINES: 153-154
QUOTE: przy definicji narzędzia bardzo ważne są dwie rzeczy. Oczywiście to jest opis schematu wejściowego, wyjściowego danego narzędzia, ale też opis tego narzędzia.
KIND: practice

ITEM: Describe the tool's function and its parameters clearly and thoroughly to minimize the chance of the model hallucinating its usage or inputs.
LESSON: L02
LINES: 155-157
QUOTE: im lepiej opiszesz, co robi dana funkcja, im lepiej opiszesz, jakie są jej parametry, tym rzadziej model będzie halucynował moment jej użycia bądź halucynował wejściowe parametry.
KIND: practice

ITEM: Include contextual hints like readOnlyHint or destructiveHint to inform the model about the nature and side effects of the tool.
LESSON: L02
LINES: 159-162
QUOTE: Możemy też dodawać pewne podpowiedzi dotyczące charakteru danego narzędzia, tak jak np. readOnlyHint, który mówi, że to narzędzie nie ma żadnych skutków ubocznych, albo destructiveHint, że to narzędzie może usuwać dane.
KIND: capability

ITEM: Include a serialized text string in the content field as a fallback, even when returning data in the StructuredContent format.
LESSON: L02
LINES: 184-186
QUOTE: nawet jeżeli wysyłacie dane w tym takim nowoczesnym, można powiedzieć, formacie StructuredContent, to dla klientów i tak często musimy zwracać tą wersję tekstową w formie content.
KIND: practice

ITEM: Avoid returning JSON-RPC protocol-level errors for application-level issues, such as a missing database record.
LESSON: L02
LINES: 195-197
QUOTE: jeżeli np. narzędzie nie znajdzie jakiegoś użytkownika w bazie, to nie powinniście zwracać błędu na poziomie protokołu JSON-RPC, bo błąd protokołu jako taki jest błędem krytycznym.
KIND: anti-pattern

ITEM: Communicate application-level errors by returning a standard response and setting the isError field to true.
LESSON: L02
LINES: 198-199
QUOTE: Zamiast tego powinien się zwrócić normalny wynik, natomiast pole isError ustawić na true.
KIND: practice

ITEM: Push a notifications/resources/updated message from the server when you want the client to refresh live resources without waiting for a user action.
LESSON: L02
LINES: 244-247
QUOTE: serwer może wysyłać taką notyfikację notifications/resources/updated, co jest na przykład idealne, jak chcecie monitorować logi na żywo.
KIND: capability

ITEM: Do not use resources as an unlimited storage mechanism, as language models have finite context windows.
LESSON: L02
LINES: 249-250
QUOTE: jako architekci musimy pamiętać, że zasoby to nie jest nielimitowany dysk.
KIND: architecture

ITEM: Serve granular, essential fragments of data using templates instead of returning massive, unoptimized data dumps.
LESSON: L02
LINES: 256-257
QUOTE: używamy template'ów tam, gdzie możemy, żeby serwować tylko małe, te niezbędne fragmenty danych, a nie całe wielkie dumpy.
KIND: practice

ITEM: Implement pagination with parameters to allow the model to fetch and scroll through long lists piece by piece.
LESSON: L02
LINES: 258-259
QUOTE: możemy stosować paginację, czyli jeśli lista jest za długa, to mamy parametr, który pozwala modelowi przewijać kawałek po kawałku te komponenty.
KIND: capability

ITEM: Be highly cautious with binary data, as it consumes context capacity much faster than lines of code.
LESSON: L02
LINES: 261
QUOTE: Pamiętajmy też, że dane binarne bardzo zżerają kontekst.
KIND: practice

ITEM: Expose a specific tool for searching large datasets instead of relying on the AI to locate information within a bulk resource.
LESSON: L02
LINES: 265-267
QUOTE: jeżeli chcesz, żeby AI przeszukała jakiś wielki zbiór danych, to utwórz do tego narzędzie, czyli użyj Tools, a nie licz, że odnajdzie to w zasobie.
KIND: practice

ITEM: Rely predominantly on tools for interaction to ensure the server-host communication remains visible and available to the model within the chat window.
LESSON: L02
LINES: 273-275
QUOTE: w przypadku MCP musimy opierać się maksymalnie na narzędziach, żeby ta interakcja MCP Server z MCP Host w maksymalnym stopniu była dostępna w danym oknie czatu i była dostępna dla modelu.
KIND: architecture

ITEM: Send a PromptListChanged notification after updating a prompt so the host can refresh the logic immediately without requiring a connection restart.
LESSON: L02
LINES: 292-293
QUOTE: jeżeli chcemy zmienić sposób, w jaki agent obsługuje błędy, aktualizujemy ten prompt i wysyłamy powiadomienie PromptListChanged
KIND: lifecycle

ITEM: Utilize MCP Apps rather than Tools when the output requires user interactions such as clicking, filtering data, or submitting forms.
LESSON: L02
LINES: 320-322
QUOTE: Jeżeli wynik wymaga od użytkownika klikania, filtrowania danych, wypełniania formularzy, no to App będzie, najprawdopodobniej, bo jest to dość nowy standard, lepsze od Tools
KIND: capability

ITEM: Filter Sampling requests on the host to ensure the server cannot maliciously extract confidential data from the chat history.
LESSON: L02
LINES: 343-345
QUOTE: MCP Host ma tak na to obowiązek filtrować te prośby o Sampling, żeby serwer nie próbował na przykład wyłudzać jakichś poufnych danych z historii czatu.
KIND: security

ITEM: Employ the Sampling feature when the server needs an AI to make decisions, such as classifying data, before returning a result.
LESSON: L02
LINES: 347-348
QUOTE: Użyj tego, kiedy na przykład serwer musi podjąć jakieś decyzje typu sklasyfikowanie jakichś danych przed zwróceniem ich.
KIND: capability

ITEM: Base your design only on primitives that your target clients actually support to avoid deploying a server that is unusable for certain users.
LESSON: L02
LINES: 398-401
QUOTE: upewnić się, że opierasz się o te konkretne prymitywy, które funkcjonują w Twoich klientach, żeby nie odciąć części użytkowników albo nie spowodować, że wdrożysz serwer, który dla części użytkowników będzie całkowicie niestrawny.
KIND: architecture

ITEM: Use SSE for remote communication when the server primarily needs to push proactive updates to the client.
LESSON: L02
LINES: 416-418
QUOTE: Mamy dostępne SSE i to powinniśmy wykorzystać, kiedy serwer głównie wysyła aktualizacje do klienta, bo potrzebuje aktualizacji, o której MCP Client pasywnie nie pyta
KIND: architecture

ITEM: Select Stateless mode only for simple tools that do not involve complex server-side logic or long-running operations requiring notifications.
LESSON: L02
LINES: 434-437
QUOTE: tryb Stateless powinniśmy wybrać tylko wtedy, kiedy nasze narzędzia są proste, nie wymagają jakiegoś myślenia po stronie serwera czy długotrwałych operacji z powiadomieniami.
KIND: architecture

ITEM: Utilize JSON Response Mode when you only require standard JSON responses and do not need streaming capabilities.
LESSON: L02
LINES: 439-441
QUOTE: Jeżeli nie potrzebujemy streamingu, czyli potrzebujemy czystego JSON-a, możemy użyć JSON Response Mode.
KIND: architecture

ITEM: Choose the stdio transport method when establishing local communication between processes.
LESSON: L02
LINES: 448-449
QUOTE: jeżeli chcesz pracować lokalnie, no to oczywiście używasz stdio.
KIND: architecture

ITEM: Implement Streamable HTTP for remote integrations with SaaS platforms.
LESSON: L02
LINES: 449
QUOTE: Jeżeli pracujesz zdalnie z jakimś SaaS-em, używasz Streamable HTTP.
KIND: architecture

ITEM: Ensure Session Affinity is configured in your infrastructure when using Stateful mode for advanced features like Sampling, subscriptions, or Progress Tracking.
LESSON: L02
LINES: 450-452
QUOTE: jeżeli potrzebujesz pełnej mocy, czyli Sampling, subskrypcji, Progress Tracking i tak dalej, to wybierasz tryb Stateful i musisz wtedy zapewnić Session Affinity, czyli stickiness na swojej infrastrukturze.
KIND: architecture

ITEM: Select Stateless mode to prioritize horizontal scaling and simplicity, accepting the lack of advanced interactive features.
LESSON: L02
LINES: 452-454
QUOTE: Jeżeli priorytetem jest skalowanie horyzontalne, prostota, wybierasz tryb Stateless i akceptujesz brak tych zaawansowanych funkcji interaktywnych.
KIND: architecture

ITEM: Include a WWW-Authenticate header containing the resource_metadata URL when returning a 401 Unauthorized response.
LESSON: L03
LINES: 494-495
QUOTE: ten 401 musi zawierać header WWW-Authenticate z URL-em do resource_metadata.
KIND: obligation

ITEM: Verify that the presented OAuth token was issued specifically for your server by implementing Audience Binding.
LESSON: L03
LINES: 539-540
QUOTE: MCP Server powinien sprawdzić, czy token został wystawiony dokładnie dla tego serwera.
KIND: security

ITEM: Issue short-lived access tokens so their validity and user consent are frequently re-checked during the refresh token rotation.
LESSON: L03
LINES: 543-546
QUOTE: ten access token powinien żyć w miarę krótko po to, żeby na poziomie regeneracji refresh tokena moglibyśmy sprawdzić, czy ten token przynajmniej nie został zinwalidowany albo czy użytkownik już nie wycofał tego poświadczenia.
KIND: security

ITEM: Always enforce the use of PKCE with the S256 algorithm to maintain security standards.
LESSON: L03
LINES: 552-554
QUOTE: PKCE z obowiązkowym S256 jest niezmiennie wymaganym algorytmem do zapewnienia bezpieczeństwa.
KIND: security

ITEM: Validate the state parameter and strictly bind the user's browser session to the initiated login process to prevent session hijacking.
LESSON: L03
LINES: 563-565
QUOTE: Nie było bindowania stanu czy weryfikowania parametru state, i sesja użytkownika w przeglądarce nie była sztywnie powiązana z zainicjowanym procesem logowania.
KIND: security

ITEM: Apply the principle of least privilege by generating highly granular permissions per resource or repository to limit the blast radius.
LESSON: L03
LINES: 595-598
QUOTE: stosując minimalizację uprawnień, generować bardzo granularne uprawnienia do poszczególnego jednego zasobu, do poszczególnego repozytorium, po to, żeby ograniczać tak zwany Blast Radius.
KIND: security

ITEM: Implement supplementary permissions specifically for reading personal data to prevent its accidental exposure to the model.
LESSON: L03
LINES: 599-601
QUOTE: Można na przykład wprowadzać dodatkowe uprawnienia do odczytywania danych osobowych, po to, żeby dodatkowo chronić je przed przypadkowym wyciekiem do modelu.
KIND: security

ITEM: Verify the JWT signature on the server for each request to ensure it originates from the private key owner under the Demonstrated Proof of Possession mechanism.
LESSON: L03
LINES: 611-613
QUOTE: przy każdym żądaniu MCP Client będzie musiał wygenerować i podpisać ten obiekt JWT, po to, żeby serwer mógł sprawdzić podpis i upewnić się, że żądanie pochodzi od właściciela klucza prywatnego
KIND: security
