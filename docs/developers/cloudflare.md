### CORS
[Configuring CORS in cloudflare](https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/cors/#allow-preflighted-requests)
documentation covers several methods, particularly with CORS pre-flight requests, for
effectively controlling CORS and preventing issues.

### Application Audience (AUD) Tag

Cloudflare Access applications have a dynamically generated AUD tag which will need to
be used by any services (e.g. API) to authenticate a Cloudflare Access generated JWT.

The online [documentation](https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/#get-your-aud-tag)
describes where to find the AUD with examples of decoding Cloudflare's JWTs in Go,
Python, and Javascript.

### Team Domain

The 'team domain' is another unique piece of information used by cloudflare's SDKs to
do things like dynamically retrieve the appropriate client PKI keys for a cloudflare
zero-trust application. This information can be retrieved from the
[zero-trust dashboard](https://one.dash.cloudflare.com/) under `Settings > Custom Pages`.