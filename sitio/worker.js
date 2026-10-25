// Pequeño programa de Cloudflare que solo atiende /video/*: entrega los videos por partes ("Range"),
// algo que iPhone y Safari exigen para reproducirlos. Todo lo demás lo sirven los archivos estáticos.
export default {
  async fetch(request, env) {
    const rango = request.headers.get("Range");
    const sinRango = new Request(request.url, { method: request.method, headers: { Accept: request.headers.get("Accept") || "*/*" } });
    const respuesta = await env.ASSETS.fetch(sinRango);
    if (!rango || respuesta.status !== 200) return respuesta;

    const datos = await respuesta.arrayBuffer();
    const total = datos.byteLength;
    const m = /^bytes=(\d*)-(\d*)$/.exec(rango.trim());
    let inicio = m && m[1] !== "" ? Number(m[1]) : NaN;
    let fin = m && m[2] !== "" ? Number(m[2]) : total - 1;
    if (m && m[1] === "" && m[2] !== "") {
      inicio = Math.max(total - Number(m[2]), 0);
      fin = total - 1;
    }
    const cabeceras = new Headers(respuesta.headers);
    cabeceras.set("Accept-Ranges", "bytes");
    if (!m || Number.isNaN(inicio) || inicio >= total || fin < inicio) {
      cabeceras.set("Content-Range", `bytes */${total}`);
      cabeceras.delete("Content-Length");
      return new Response(null, { status: 416, headers: cabeceras });
    }
    fin = Math.min(fin, total - 1);
    cabeceras.set("Content-Range", `bytes ${inicio}-${fin}/${total}`);
    cabeceras.set("Content-Length", String(fin - inicio + 1));
    const cuerpo = request.method === "HEAD" ? null : datos.slice(inicio, fin + 1);
    return new Response(cuerpo, { status: 206, headers: cabeceras });
  },
};
