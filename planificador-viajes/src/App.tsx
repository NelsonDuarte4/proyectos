import { useState, type FormEvent } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

interface Destino {
  id: number;
  ciudad: string;
  pais: string;
  fechaInicio: string;
  duracionDias: number;
  clima?: string;
  lat: number;
  lng: number;
}

// Componente auxiliar para mover la cámara del mapa suavemente
function CambiarVistaMapa({ centro }: { centro: [number, number] }) {
  const mapa = useMap()
  mapa.setView(centro, 6, { animate: true }) // Zoom intermedio (6) para ver bien la región
  return null
}

function App() {
  // Destino inicial (Asunción)
  const [misDestinos, setMisDestinos] = useState<Destino[]>([
    { id: 1, ciudad: "Asunción", pais: "Paraguay", fechaInicio: "2026-06-15", duracionDias: 5, clima: "☀️ 28°C", lat: -25.2637, lng: -57.5759 }
  ])

  // Estados del formulario
  const [nuevaCiudad, setNuevaCiudad] = useState<string>('')
  const [nuevoPais, setNuevoPais] = useState<string>('')
  const [nuevaFecha, setNuevaFecha] = useState<string>('')
  const [nuevaDuracion, setNuevaDuracion] = useState<number>(1)
  const [cargando, setCargando] = useState<boolean>(false)
  
  // El centro inicial del mapa
  const [centroMapa, setCentroMapa] = useState<[number, number]>([-25.2637, -57.5759])

  // Función para consultar el clima en tiempo real (wttr.in)
  const obtenerClima = async (ciudad: string): Promise<string> => {
    try {
      const respuesta = await fetch(`https://wttr.in/${ciudad}?format=j1`)
      if (!respuesta.ok) throw new Error()
      const datos = await respuesta.json()
      const temp = datos.current_condition[0].temp_C
      const infoClima = datos.current_condition[0].lang_es?.[0]?.value || datos.current_condition[0].weatherDesc[0].value
      return `🌡️ ${temp}°C — ${infoClima}`
    } catch {
      return "🤷 Clima no disponible"
    }
  }

  // Manejador del formulario (Búsqueda inteligente por campos separados)
  const manejarAgregarDestino = async (e: FormEvent) => {
    e.preventDefault()
    if (!nuevaCiudad.trim() || !nuevoPais.trim() || !nuevaFecha) return

    setCargando(true)

    try {
      // 1. Buscamos el clima de la ciudad
      const climaObtenido = await obtenerClima(nuevaCiudad)

      // 2. Intento 1: Buscamos estructurado (separando ciudad y país para máxima precisión)
      const urlAPI = `https://nominatim.openstreetmap.org/search?format=json&city=${encodeURIComponent(nuevaCiudad)}&country=${encodeURIComponent(nuevoPais)}&limit=1`
      
      const respuestaGeo = await fetch(urlAPI, {
        headers: { 'Accept-Language': 'es,en' } // Prioriza nombres en español o inglés
      })
      const datosGeo = await respuestaGeo.json()

      let lat = 0
      let lng = 0

      if (datosGeo && datosGeo.length > 0) {
        lat = parseFloat(datosGeo[0].lat)
        lng = parseFloat(datosGeo[0].lon)
      } else {
        // Intento 2: Si falló el anterior, hacemos una búsqueda libre general (más flexible)
        const urlAlternativa = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(`${nuevaCiudad} ${nuevoPais}`)}&limit=1`
        const resAlt = await fetch(urlAlternativa)
        const datosAlt = await resAlt.json()
        
        if (datosAlt && datosAlt.length > 0) {
          lat = parseFloat(datosAlt[0].lat)
          lng = parseFloat(datosAlt[0].lon)
        } else {
          alert(`⚠️ No pudimos localizar "${nuevaCiudad}, ${nuevoPais}" en el mapa. Revisa cómo está escrito.`)
        }
      }

      // Si encontramos coordenadas válidas (distintas de 0), agregamos el destino
      if (lat !== 0 && lng !== 0) {
        const nuevoDestino: Destino = {
          id: Date.now(),
          ciudad: nuevaCiudad,
          pais: nuevoPais,
          fechaInicio: nuevaFecha,
          duracionDias: nuevaDuracion,
          clima: climaObtenido,
          lat: lat,
          lng: lng
        }

        setMisDestinos([...misDestinos, nuevoDestino])
        setCentroMapa([lat, lng]) // Mueve la cámara al nuevo lugar
      }

    } catch (error) {
      console.error("Error al procesar el destino:", error)
      alert("Hubo un problema de conexión al buscar el lugar.")
    }

    // Reseteamos los campos del formulario
    setCargando(false)
    setNuevaCiudad('')
    setNuevoPais('')
    setNuevaFecha('')
    setNuevaDuracion(1)
  }

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', fontFamily: 'sans-serif', color: '#fff', background: '#111', margin: 0, overflow: 'hidden' }}>
      
      {/* PANEL IZQUIERDO: FORMULARIO Y LISTA */}
      <div style={{ width: '400px', minWidth: '400px', padding: '20px', overflowY: 'auto', borderRight: '1px solid #333', boxSizing: 'border-box' }}>
        <h1>🌍 Planificador Global</h1>
        <p style={{ color: '#aaa' }}>Busca cualquier lugar del mundo y mira el mapa.</p>
        
        <form onSubmit={manejarAgregarDestino} style={{ display: 'flex', flexDirection: 'column', gap: '10px', background: '#1a1a1a', padding: '15px', borderRadius: '8px' }}>
          <input type="text" placeholder="Ciudad (Ej: Tokyo, Rio de Janeiro, Paris)" value={nuevaCiudad} onChange={(e) => setNuevaCiudad(e.target.value)} style={{ padding: '8px', borderRadius: '4px', border: '1px solid #444', background: '#222', color: '#fff' }} />
          <input type="text" placeholder="País (Ej: Japon, Brasil, Francia)" value={nuevoPais} onChange={(e) => setNuevoPais(e.target.value)} style={{ padding: '8px', borderRadius: '4px', border: '1px solid #444', background: '#222', color: '#fff' }} />
          <div style={{ display: 'flex', gap: '10px' }}>
            <input type="date" value={nuevaFecha} onChange={(e) => setNuevaFecha(e.target.value)} style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #444', background: '#222', color: '#fff' }} />
            <input type="number" min="1" value={nuevaDuracion} onChange={(e) => setNuevaDuracion(Number(e.target.value))} style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #444', background: '#222', color: '#fff' }} />
          </div>
          <button type="submit" disabled={cargando} style={{ padding: '10px', background: '#646cff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
            {cargando ? 'Buscando Destino...' : 'Agregar Destino'}
          </button>
        </form>

        <h3 style={{ marginTop: '20px' }}>Tus Destinos (Haz clic para viajar):</h3>
        {misDestinos.map(destino => (
          <div key={destino.id} onClick={() => setCentroMapa([destino.lat, destino.lng])} style={{ background: '#222', padding: '12px', borderRadius: '8px', margin: '10px 0', border: '1px solid #333', cursor: 'pointer', transition: 'background 0.2s' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong>{destino.ciudad}, {destino.pais}</strong>
              <span style={{ fontSize: '12px', color: '#646cff' }}>{destino.clima}</span>
            </div>
            <div style={{ fontSize: '12px', color: '#aaa', marginTop: '5px' }}>📅 {destino.fechaInicio} ({destino.duracionDias} días)</div>
          </div>
        ))}
      </div>

      {/* PANEL DERECHO: MAPA EN VIVO */}
      <div style={{ flex: 1, height: '100vh', position: 'relative' }}>
        <MapContainer center={centroMapa} zoom={4} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='&copy; OpenStreetMap' />
          <CambiarVistaMapa centro={centroMapa} />
          {misDestinos.map(destino => (
            destino.lat !== 0 && destino.lng !== 0 && (
              <Marker key={destino.id} position={[destino.lat, destino.lng]}>
                <Popup><div style={{ color: '#000' }}><strong>{destino.ciudad}</strong><br />{destino.clima}</div></Popup>
              </Marker>
            )
          ))}
        </MapContainer>
      </div>

    </div>
  )
}

export default App