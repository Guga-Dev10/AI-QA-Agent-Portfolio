import asyncio
import time
import statistics
import aiohttp

TARGET_URL = "https://example.com"
CONCURRENT_USERS = 5
TEST_DURATION_SECONDS = 10

class LoadTestRunner:
    def __init__(self, url, users, duration):
        self.url = url
        self.users = users
        self.duration = duration
        self.results = []
        self.errors = []

    async def user_worker(self, user_id, stop_time, session):
        while time.time() < stop_time:
            start_req = time.perf_counter()
            try:
                async with session.get(self.url) as response:
                    await response.read()
                    elapsed = (time.perf_counter() - start_req) * 1000  # ms
                    self.results.append({
                        "user_id": user_id,
                        "status": response.status,
                        "latency_ms": elapsed,
                        "success": 200 <= response.status < 400
                    })
            except Exception as e:
                elapsed = (time.perf_counter() - start_req) * 1000
                self.errors.append(str(e))
                self.results.append({
                    "user_id": user_id,
                    "status": 0,
                    "latency_ms": elapsed,
                    "success": False
                })
            # Small delay to prevent tight loop overload
            await asyncio.sleep(0.01)

    async def run(self):
        print(f"--- INICIANDO TESTE DE CARGA ---")
        print(f"Alvo: {self.url}")
        print(f"Usuarios Concorrentes: {self.users}")
        print(f"Duracao: {self.duration} segundos")
        print("Executando...\n")

        start_test_time = time.time()
        stop_time = start_test_time + self.duration

        async with aiohttp.ClientSession() as session:
            tasks = [self.user_worker(i + 1, stop_time, session) for i in range(self.users)]
            await asyncio.gather(*tasks)

        total_test_duration = time.time() - start_test_time
        return self.generate_report(total_test_duration)

    def generate_report(self, actual_duration):
        total_requests = len(self.results)
        if total_requests == 0:
            return "Nenhuma requisicao foi completada."

        successful_requests = sum(1 for r in self.results if r["success"])
        failed_requests = total_requests - successful_requests
        latencies = [r["latency_ms"] for r in self.results]

        latencies_sorted = sorted(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)
        avg_lat = statistics.mean(latencies)
        
        def percentile(p):
            idx = int(len(latencies_sorted) * p)
            return latencies_sorted[min(idx, len(latencies_sorted) - 1)]

        p50 = percentile(0.50)
        p90 = percentile(0.90)
        p95 = percentile(0.95)
        p99 = percentile(0.99)

        rps = total_requests / actual_duration

        report = f"""
================================================================================
                    RELATORIO FINAL DE DESEMPENHO E CARGA
================================================================================
Target URL:                  {self.url}
Usuarios Concorrentes (VUs):  {self.users}
Duracao Planejada:           {self.duration} segundos
Duracao Real:                {actual_duration:.2f} segundos

--- REQUISICOES ---
Total de Requisicoes:        {total_requests}
Requisicoes com Sucesso:     {successful_requests} ({successful_requests/total_requests*100:.2f}%)
Requisicoes com Falha:       {failed_requests} ({failed_requests/total_requests*100:.2f}%)
Vazao (Throughput):          {rps:.2f} req/s

--- TEMPOS DE RESPOSTA (LATENCIA em ms) ---
Minima:                      {min_lat:.2f} ms
Media:                       {avg_lat:.2f} ms
Mediana (P50):               {p50:.2f} ms
Percentil 90 (P90):          {p90:.2f} ms
Percentil 95 (P95):          {p95:.2f} ms
Percentil 99 (P99):          {p99:.2f} ms
Maxima:                      {max_lat:.2f} ms
================================================================================
"""
        return report

if __name__ == "__main__":
    runner = LoadTestRunner(TARGET_URL, CONCURRENT_USERS, TEST_DURATION_SECONDS)
    report = asyncio.run(runner.run())
    print(report)
