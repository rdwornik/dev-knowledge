Consumers: `[#784]` (the row this evidence serves), `[#696]` (the locator defect it answers)

# agy leg -- prompt_l3.txt
# model: gemini-3.1-pro-high
# invocation: agy --model gemini-3.1-pro-high --output-format json --print-timeout 20m --dangerously-skip-permissions --print=<prompt_l3.txt>
# exit: 0 | wall: 72.8s | status: SUCCESS | usage: {'input_tokens': 13006, 'output_tokens': 11813, 'thinking_tokens': 10533, 'cache_read_tokens': 20266, 'total_tokens': 24819}
# ordered reader, not substituted

ITEM: Define your server capabilities, such as Tools, Prompts, and Resources.
LESSON: L06
LINES: 1038-1040
QUOTE: mamy tutaj tak naprawdę możliwość zdefiniowania. Po pierwsze, jakie capabilities będzie zawierał nasz serwer, czyli mamy Tools, mamy Prompts, mamy Resources.
KIND: capability

ITEM: Describe tool schemas accurately so that the LLM knows what information to expect.
LESSON: L06
LINES: 1053-1055
QUOTE: Tak naprawdę musi być bardzo dokładnie opisane, żeby LLM wiedział, jakich informacji się spodziewać.
KIND: obligation

ITEM: Expose a controller that returns /.well-known/ metadata, such as the resource, Authorization Server, and supported scopes.
LESSON: L06
LINES: 1065-1067
QUOTE: Dodatkowo mamy kontroler, który zwraca nam te informacje /.well-known/, takie jak resource, Authorization Server, scope'y, jakie są wspierane i tak dalej.
KIND: architecture

ITEM: Return a 401 status code for unauthenticated requests, in accordance with the specification.
LESSON: L06
LINES: 1094-1095
QUOTE: Możemy wejść na ten URL i zobaczymy, że tutaj dostaniemy 401, czyli tak jak powinno być zgodnie ze specyfikacją.
KIND: obligation

ITEM: Return a 401 response with a header that indicates the location of all metadata when a request fails authentication.
LESSON: L06
LINES: 1099-1101
QUOTE: mamy POST'a do mojego MCP Server, który zwraca 401 razem z tym headerem, który mówi: no niestety nie udało się, ale tutaj masz informację o tym, gdzie są wszystkie metadane.
KIND: practice

ITEM: Be aware that requests from the LLM to the MCP server might be blocked by WAFs as malicious bot traffic.
LESSON: L06
LINES: 1120-1124
QUOTE: jeżeli po wykonaniu tego żądania nie widzielibyście dalej odwołań do MCP, one prawdopodobnie są blokowane jako złośliwy ruch, ponieważ Cloudflare i inne WAF-y potrafią wycinać cały ruch, który idzie od Claude'a. Tutaj to jeszcze nie jest wykrywane jako ruch botów, natomiast to, co idzie do MCP, idzie bezpośrednio z LLM-a i to już jest wykrywane jako ruch bota.
KIND: observability

ITEM: Avoid passing the token directly from the MCP client to the server.
LESSON: L06
LINES: 1156-1157
QUOTE: W trakcie naszego wykładu wcześniejszego mówiliśmy o tym, że przekazywanie tokena z MCP bezpośrednio do serwera nie jest najlepszym pomysłem.
KIND: anti-pattern

ITEM: Handle authorization in the MCP server without directly passing tokens.
LESSON: L07
LINES: 1183-1184
QUOTE: w jaki sposób nasz MCP Server powinien obsługiwać autoryzację bez przekazywania tokenów.
KIND: security

ITEM: Implement a Token Introspection mechanism to check incoming tokens.
LESSON: L07
LINES: 1195-1196
QUOTE: Zaimplementujemy mechanizm Token Introspection, który ma sprawdzać te tokeny przychodzące
KIND: architecture

ITEM: Implement a Token Exchange mechanism to fetch a backend-specific token based on the token obtained from the MCP.
LESSON: L07
LINES: 1196-1198
QUOTE: i Token Exchange, który pozwoli nam pobrać na podstawie tego tokena uzyskanego z MCP bezpośrednio token dla usług backendowych.
KIND: architecture

ITEM: Implement a field or filter in the MCP Server that performs introspection on the token received directly from the MCP Server.
LESSON: L07
LINES: 1217-1218
QUOTE: mamy tutaj zaimplementowany field, który robi introspekcję tego tokena, który przychodzi z MCP Server bezpośrednio
KIND: practice

ITEM: Use a TokenExchangeClient to exchange the initial token for a new one after successful introspection.
LESSON: L07
LINES: 1218-1220
QUOTE: i jeżeli to jest ok, to tak naprawdę po zawołaniu tej introspekcji mamy TokenExchangeClient, który robi exchange tokenów i strzela po wymianę tego jednego tokena na drugi
KIND: practice

ITEM: Pass the exchanged token to the backend instead of the original one.
LESSON: L07
LINES: 1220-1221
QUOTE: i dalej wszystko idzie już tak samo, czyli też ten konkretny token wymieniony będzie przekazywany do backendu.
KIND: obligation

ITEM: Implement an IntrospectionFilter on the backend side to introspect the exchanged token it receives.
LESSON: L07
LINES: 1223-1225
QUOTE: Jeżeli chodzi o backend, też możemy sobie tutaj zobaczyć w kontekście OAuth, że mamy na przykład IntrospectionFilter, który robi nam introspekcję tego tokenu
KIND: architecture
