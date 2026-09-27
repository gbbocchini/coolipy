<%!
    # Custom <head> additions for coolipy documentation.
    # Included at the end of <head> by html.mako — owns the SEO/social/LLM
    # metadata and the Elastic APM real-user-monitoring snippet so that every
    # regenerated page ships with discoverability built in.
    description = (
        "coolipy is the (un)official, fully-typed Python client for the "
        "Coolify API — synchronous and asynchronous, wrapping every token-gated "
        "endpoint with pydantic models. Deploy applications, provision "
        "databases, and manage servers, projects, teams, deployments, tags and "
        "S3 storages from Python."
    )
    keywords = (
        "coolify, coolify api, coolify python, coolify client, coolify sdk, "
        "coolipy, python client, rest api client, async, pydantic, "
        "self-hosted paas, deployment automation"
    )
    site_url = 'https://coolipydocs.gabrielbocchini.com.br/'
%>
<meta name="description" content="${description}" />
<meta name="keywords" content="${keywords}" />
<meta name="author" content="Gabriel Bocchini" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<%
    # Every page needs a canonical: nginx serves /models/common, /models/common.html
    # and /models/ as the same document, so without one the crawlers index three
    # copies of every page. Derive the URL from the module's own dotted name,
    # which mirrors the layout pdoc writes (packages become <path>/index.html).
    _parts = module.name.split('.', 1) if 'module' in context.keys() else []
    _rel = _parts[1].replace('.', '/') if len(_parts) > 1 else ''
    if _rel:
        _rel += '/' if module.is_package else '.html'
    canonical = site_url + _rel
%>\
<link rel="canonical" href="${canonical}" />


<!-- Open Graph -->
<meta property="og:site_name" content="coolipy" />
<meta property="og:type" content="website" />
<meta property="og:title" content="coolipy — Python client for Coolify" />
<meta property="og:description" content="${description}" />
% if 'module' in context.keys() and module.name == 'coolipy':
<meta property="og:url" content="${site_url}" />
% endif

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="coolipy — Python client for Coolify" />
<meta name="twitter:description" content="${description}" />

<!-- Structured data: SoftwareApplication -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "coolipy",
  "alternateName": "Coolipy — Python client for Coolify",
  "description": "${description}",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Any",
  "programmingLanguage": "Python",
  "softwareVersion": "1.0.0",
  "license": "https://www.apache.org/licenses/LICENSE-2.0",
  "author": {
    "@type": "Person",
    "name": "Gabriel Bocchini",
    "url": "https://github.com/gbbocchini"
  },
  "publisher": {
    "@type": "Organization",
    "name": "coolipy"
  },
  "url": "${site_url}",
  "sameAs": [
    "https://github.com/gbbocchini/coolipy",
    "https://pypi.org/project/coolipy/"
  ],
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "downloadUrl": "https://pypi.org/project/coolipy/",
  "featureList": [
    "Synchronous and asynchronous clients in one package",
    "Fully typed pydantic request and response models",
    "Full coverage of the Coolify token-gated REST API",
    "Typed errors and dependency-injected HTTP transport"
  ]
}
</script>

<!-- Elastic APM real-user monitoring -->
<script src="https://coolipy-rum.s3.us-east-1.amazonaws.com/elastic-apm-rum.umd.min.js" crossorigin></script>
<script>
  elasticApm.init({
    serviceName: 'coolipy-docs',
    serverUrl: 'https://84b3afd273634acabe46950fe95c9687.apm.southamerica-east1.gcp.elastic-cloud.com:443',
  })
</script>
