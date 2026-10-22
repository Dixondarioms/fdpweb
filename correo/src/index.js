// Reenvía cada correo que llega a contacto@fdpsoftware.org a todas las direcciones de DESTINOS.
// Cada destino tiene que estar verificado en Cloudflare: Email Routing → Destination addresses.
export default {
  async email(message, env) {
    const destinos = env.DESTINOS.split(",").map((d) => d.trim()).filter(Boolean);

    // Si un destino falla, los demás igual reciben el correo
    const resultados = await Promise.allSettled(destinos.map((d) => message.forward(d)));
    const fallidos = resultados.filter((r) => r.status === "rejected");

    for (const f of fallidos) {
      console.error("No se pudo reenviar:", f.reason);
    }
    // Si no se pudo entregar a nadie, se rechaza para que el remitente sepa que no llegó
    if (fallidos.length === destinos.length) {
      message.setReject("No se pudo entregar el mensaje. Escríbenos por WhatsApp: +58 412-0846332");
    }
  },
};
