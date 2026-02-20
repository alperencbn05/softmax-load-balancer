import math
import random

class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        # Sunucunun temel gecikme süresi (10ms - 100ms arası rastgele başlar)
        self.base_latency = random.uniform(10, 100)

    def get_response_time(self):
        # Non-stationary (sabit olmayan) yapı: Zamanla sunucunun hızı rastgele değişebilir
        self.base_latency += random.uniform(-2, 2)
        self.base_latency = max(1.0, self.base_latency) # 0'ın altına düşmesin

        # Gürültülü (Noisy) yapı: Anlık dalgalanmalar eklenir
        noise = random.uniform(-5, 5)
        return max(1.0, self.base_latency + noise)

class SoftmaxLoadBalancer:
    def __init__(self, num_servers, tau=0.1):
        self.num_servers = num_servers
        self.tau = tau
        # Q değerleri (Başarı puanı): Başlangıçta tüm sunucular eşit (0.0)
        self.q_values = [0.0] * num_servers
        # Hangi sunucunun kaç kere seçildiği
        self.counts = [0] * num_servers

    def select_server(self):
        # NÜMERİK STABİLİTE ÇÖZÜMÜ: Overflow (sonsuz değer) hatasını önlemek için 
        # en büyük Q değerini buluyoruz.
        max_q = max(self.q_values)

        probabilities = []
        toplam_agirlik = 0.0
        agirliklar = []

        # Softmax Formülü
        for q in self.q_values:
            # Her bir q değerinden max_q çıkarılarak e^0 (1) en büyük değer yapılır, bellek taşmaz.
            agirlik = math.exp((q - max_q) / self.tau)
            agirliklar.append(agirlik)
            toplam_agirlik += agirlik

        # Ağırlıkları olasılığa (%'lik dilime) çevir
        for agirlik in agirliklar:
            probabilities.append(agirlik / toplam_agirlik)

        # Hesaplanmış olasılıklara göre rastgele ama bilinçli (Softmax'a dayalı) seçim yap
        secilen_sunucu = random.choices(range(self.num_servers), weights=probabilities, k=1)[0]
        return secilen_sunucu

    def update_q_value(self, server_id, latency):
        # Gecikme (latency) ne kadar düşükse, ödül (reward) o kadar yüksek olmalı
        reward = 100.0 / latency

        # Q değerini güncelleme (Hareketli ortalama formülü)
        self.counts[server_id] += 1
        n = self.counts[server_id]
        eski_q = self.q_values[server_id]

        # Yeni Q değeri = Eski Q + (1/n) * (Ödül - Eski Q)
        self.q_values[server_id] = eski_q + (1.0 / n) * (reward - eski_q)

# --- SİMÜLASYON BAŞLATICI ---
def run_simulation():
    NUM_SERVERS = 5
    TOTAL_REQUESTS = 1000

    servers = [Server(i) for i in range(NUM_SERVERS)]
    # tau (sıcaklık) parametresi keşif ve sömürü dengesini ayarlar
    load_balancer = SoftmaxLoadBalancer(NUM_SERVERS, tau=0.5)

    print("Simülasyon Başlıyor... İstekler dağıtılıyor.\n")

    for request in range(TOTAL_REQUESTS):
        # 1. Load balancer hangi sunucuya gideceğine karar verir
        chosen_server_id = load_balancer.select_server()

        # 2. Seçilen sunucuya istek atılır ve yanıt süresi (latency) alınır
        latency = servers[chosen_server_id].get_response_time()

        # 3. Load balancer, bu sonucu öğrenir ve Q değerini günceller
        load_balancer.update_q_value(chosen_server_id, latency)

    print("--- 1000 İSTEK SONRASI SİMÜLASYON SONUÇLARI ---")
    for i in range(NUM_SERVERS):
        print(f"Sunucu {i} | Toplam Yönlendirme: {load_balancer.counts[i]:>4} kez | Performans (Q) Puanı: {load_balancer.q_values[i]:.2f}")
    
    print("\nSonuç Analizi: Yük dengeleyici, Q puanı (performansı) en yüksek olan sunucuya en çok isteği yönlendirerek görevini başarıyla tamamlamıştır.")

if __name__ == '__main__':
    run_simulation()