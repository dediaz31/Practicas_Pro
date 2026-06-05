export default function Page() {
  return (
    <main style={{ minHeight: '100vh', padding: '4rem 1rem', background: 'linear-gradient(180deg, #eef2ff 0%, #ffffff 100%)' }}>
      <div style={{ maxWidth: 720, margin: '0 auto', textAlign: 'center', padding: '3rem', background: '#ffffff', borderRadius: 24, boxShadow: '0 28px 70px rgba(15, 23, 42, 0.08)' }}>
        <p style={{ marginBottom: '0.75rem', color: '#2563eb', fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', fontSize: '0.8rem' }}>PrácticasPro</p>
        <h1 style={{ fontSize: '2.5rem', margin: '0 0 1rem', lineHeight: 1.1 }}>Usa la app principal en FastAPI</h1>
        <p style={{ color: '#475569', fontSize: '1rem', lineHeight: 1.75, marginBottom: '2rem' }}>
          Esta página es un proyecto adicional. La aplicación principal se ejecuta en <strong>http://localhost:8000</strong> y ofrece la interfaz profesional de gestión de prácticas.
        </p>
        <a href="http://localhost:8000" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', padding: '0.85rem 1.5rem', borderRadius: 9999, background: '#2563eb', color: '#ffffff', textDecoration: 'none', fontWeight: 600 }}>Abrir app principal</a>
      </div>
    </main>
  )
}
