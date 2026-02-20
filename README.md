# softmax-load-balancer
# Client-Side Load Balancer with Softmax Action Selection

## Proje Hakkında
Bu proje, K adet farklı sunucudan (server) oluşan bir kümeye gelen istekleri dağıtmak için tasarlanmış bir istemci taraflı (client-side) yük dengeleyicidir. Sistemdeki sunucuların yanıt süreleri sabit değildir (non-stationary) ve rastgele dalgalanmalar (noisy) gösterir. 

Amacımız, toplam bekleme süresini (latency) minimize eden, sisteme dinamik olarak adapte olabilen otonom bir dağıtım mimarisi kurmaktır.

## Kullanılan Algoritma: Neden Softmax?
Geleneksel **Round-Robin** algoritması sunucuların anlık performans durumlarını umursamadan sırayla dağıtım yapar; **Random** algoritması ise kontrolsüzdür. Bu iki yöntem de çöken veya anlık yavaşlayan bir sunucuyu tespit edip yükü oradan çekemez.

Bu projede **Softmax Action Selection** (Çok Kollu Canavar / Multi-Armed Bandit problemi çözümü) kullanılmıştır. Softmax, geçmiş performansa dayalı olasılıksal bir seçim yapar:
* **Sömürü (Exploitation):** Çoğunlukla en hızlı yanıt veren sunucuya yönelir.
* **Keşif (Exploration):** Düşük bir ihtimalle de olsa diğer sunucuları yoklayarak ("tau" sıcaklık parametresi ile), performanslarının düzelip düzelmediğini test eder.

## Teknik Çözümler ve Analizler

### 1. Nümerik Stabilite Problemi ve Çözümü
Softmax algoritmasında olasılıklar hesaplanırken üstel fonksiyon ($e^x$) kullanılır. Geçmiş performans (Q) değerleri büyüdükçe bu hesaplama **Overflow** (bellek taşması) ve `NaN` (Not a Number) hatalarına yol açar. 
Bu projede nümerik stabiliteyi sağlamak için; hesaplamadan önce Q değerlerinin en büyüğü ($Q_{max}$) bulunmuş ve formüldeki tüm değerlerden çıkarılmıştır. Bu sayede hesaplanan en yüksek üs değeri $e^0 = 1$ seviyesine çekilerek donanımsal taşmaların önüne geçilmiştir.

### 2. Çalışma Zamanı (Runtime) Analizi
* **Sunucu Seçimi (select_server):** $K$ adet sunucu için ağırlık hesaplaması yapıldığından zaman karmaşıklığı **$O(K)$**'dır.
* **Performans Güncelleme (update_q_value):** İşlem bitiminde sadece ilgili sunucunun indeksine gidilerek matematiksel güncelleme yapıldığı için zaman karmaşıklığı **$O(1)$**'dir. Sistem, sunucu sayısı artsa dahi yüksek performansla çalışacak şekilde optimize edilmiştir.

## Kurulum ve Çalıştırma
Projeyi çalıştırmak için bilgisayarınızda Python yüklü olmalıdır.

1. Repoyu bilgisayarınıza klonlayın.
2. Terminal (veya komut satırı) üzerinden projenin bulunduğu dizine gidin.
3. Aşağıdaki komutu çalıştırarak simülasyonu başlatın:
   ```bash
4-  python main.py
Terminal ekranında 1000 istek sonucunda ajanın yük dağılımını nasıl optimize ettiğini görebilirsiniz.


