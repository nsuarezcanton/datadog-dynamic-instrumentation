# datadog-dynamic-instrumentation

This playground provides an environment to showcase: (a) tracing Python micro-services, (b) how adding delay to services (upstream and downstream) affects the latency metric, [trace.<SPAN_NAME>](https://docs.datadoghq.com/tracing/metrics/metrics_namespace/#latency-distribution), and (c) Datadog's [Remote Configuration](https://docs.datadoghq.com/agent/remote_config/?tab=configurationyamlfile) features.

It spins up three containers, a Redis instance, and a Datadog Agent:

- `upstream` which will appear as `upstream-flask` in Datadog.
- `downstream` which will appear as `downstream-flask`.
- `traffic` sends requests to `upstream-flask` to simulate traffic.

## Requirements

- [nerdctl](https://github.com/containerd/nerdctl). It can easily be run with [Docker](https://www.docker.com/) though.

## Getting Started

There's limited setup, we just need to add and API key:

1. Head over to the API keys page ([US](https://app.datadoghq.com/organization-settings/api-keys) or [EU](https://app.datadoghq.eu/organization-settings/api-keys) depending on your organizations's [Datadog site](https://docs.datadoghq.com/getting_started/site/)).
2. Create a new API key and give it a name of your choice.
3. Substitute `your API key` in the command below with the key you just created — it does not require quotation marks.
4. Similarly, substitute `<datadoghq.com|datadoghq.eu>` with the respective site (e.g `DD_SITE=datadoghq.eu`).

```bash
make init DD_API_KEY=<your API key> DD_SITE=<datadoghq.com|datadoghq.eu>
```

Now that we've added an API key, let's double-check that we can start up the services (i.e. containers) defined in our Docker Compose file. To start up the services, run:

```bash
make up
```

About a couple of minutes after doing this, you should see [traces](https://app.datadoghq.com/apm/traces?query=%40_top_level%3A1%20env%3Adev%20service%3Aupstream-flask&cols=core_service%2Ccore_resource_name%2Clog_duration%2Clog_http.method%2Clog_http.status_code&historicalData=false&messageDisplay=inline&sort=desc&start=1660055623242&end=1660056523242&paused=false) coming through in your Datadog account.

If you'd like to take a look at the logs, you can run:

```bash
make logs
```

To stop the services, run:

```bash
make destroy
```

## Usage

- `GET http://localhost:8100/delay/<float>` — will add a delay of `<float>` to the upstream service (e.g. `GET http://localhost:8100/delay/0.25` will set a delay of 0.25 in the upstream service).
- `GET http://localhost:8110/delay/<float>` - same behavior as above but for the downstream service.