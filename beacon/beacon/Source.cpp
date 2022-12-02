#include "WinHttp.h"

BOOL  bResults = FALSE;
HINTERNET hSession = NULL,
hConnect = NULL,
hRequest = NULL;

// Use WinHttpOpen to obtain a session handle.
hSession = WinHttpOpen(L"A WinHTTP Example Program/1.0",
    WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
    WINHTTP_NO_PROXY_NAME,
    WINHTTP_NO_PROXY_BYPASS, 0);

// Specify an HTTP server.
if (hSession)
hConnect = WinHttpConnect(hSession, L"http://192.168.1.254:8000",
    INTERNET_DEFAULT_HTTP_PORT, 0);

// Create an HTTP Request handle.
if (hConnect)
hRequest = WinHttpOpenRequest(hConnect, L"GET",
    NULL, WINHTTP_NO_REFERER,
    WINHTTP_DEFAULT_ACCEPT_TYPES,
    0);

// Send a Request.
if (hRequest)
bResults = WinHttpSendRequest(hRequest,
    WINHTTP_NO_ADDITIONAL_HEADERS,
    0, WINHTTP_NO_REQUEST_DATA, 0,
    0, 0);

// Place additional code here.


// Report errors.
if (!bResults)
printf("Error %d has occurred.\n", GetLastError());

// Close open handles.
if (hRequest) WinHttpCloseHandle(hRequest);
if (hConnect) WinHttpCloseHandle(hConnect);
if (hSession) WinHttpCloseHandle(hSession);