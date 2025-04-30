# MEV'S ISTQB AI TESTING EXAM PREP

Bu proje, ISTQB AI Tester sınavına hazırlananlar için geliştirilmiş bir Chatbot uygulamasıdır. Kullanıcılar, PDF formatındaki syllabus'u yükleyerek, içerisindeki bilgilerle ilgili sorular sorabilir ve yanıt alabilirler.

## Özellikler
- PDF dosyalarından metin çıkarma
- Metni küçük parçalara ayırarak işleme
- OpenAI'nin dil modeliyle sorulara cevap verme
- FAISS kullanarak hızlı metin araması yapma
- Streamlit ile web tabanlı arayüz

## Gereksinimler
Bu projeyi çalıştırmadan önce aşağıdaki kütüphanelerin yüklü olduğundan emin olun:

```bash
pip install streamlit PyPDF2 pdfplumber langchain faiss-cpu openai
```

```bash
OPENAI_API_KEY='your-api-key-here'
```

## Kullanım
1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/proje-adi.git
   cd proje-adi
   ```
2. Gerekli bağımlılıkları yükleyin.
3. Uygulamayı başlatın:
   ```bash
   streamlit run app.py
   ```
4. Web tarayıcınızda açılan arayüzden PDF dosyanızı yükleyin ve sorularınızı yazın.

## Ekran Görüntüsü
(![Ekran Alıntısı](https://github.com/user-attachments/assets/05b11957-f7ea-45c1-b469-cecdce3c8d72)
)

## Geliştirme Süreci
Bu proje, ISTQB AI Tester sınavına hazırlanırken geliştirilmiş olup, metin analizi ve OpenAI tabanlı chatbot entegrasyonu üzerine deneyim kazandırmayı amaçlamaktadır.

## Katkıda Bulunma
Herhangi bir geri bildiriminiz veya öneriniz varsa, GitHub üzerinden bir issue açabilirsiniz!

