import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { TILE_ATTRIBUTION, TILE_URL_TEMPLATE } from "../lib/config";

interface Props {
  lat: number;
  lng: number;
}

/** 3D 地球儀。遠景から回り込みながらマッチ地点へ降下する。 */
export default function GlobeView({ lat, lng }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current!;
    const map = new maplibregl.Map({
      container,
      style: {
        version: 8,
        projection: { type: "globe" },
        sources: {
          satellite: {
            type: "raster",
            tiles: [
              TILE_URL_TEMPLATE.replace("{z}", "{z}").replace("{y}", "{y}").replace("{x}", "{x}"),
            ],
            tileSize: 256,
            maxzoom: 14,
            attribution: TILE_ATTRIBUTION,
          },
        },
        layers: [
          { id: "background", type: "background", paint: { "background-color": "#07090f" } },
          { id: "satellite", type: "raster", source: "satellite" },
        ],
        sky: {
          "atmosphere-blend": ["interpolate", ["linear"], ["zoom"], 0, 1, 6, 0.4],
        },
      },
      center: [lng - 100, 5],
      zoom: 1.2,
      attributionControl: { compact: true },
      interactive: true,
    });

    // マッチ地点のパルスマーカー
    const el = document.createElement("div");
    el.className = "globe-marker";
    new maplibregl.Marker({ element: el }).setLngLat([lng, lat]).addTo(map);

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    map.once("load", () => {
      if (reduceMotion) {
        map.jumpTo({ center: [lng, lat], zoom: 5.8 });
        return;
      }
      window.setTimeout(() => {
        map.flyTo({
          center: [lng, lat],
          zoom: 5.8,
          duration: 7000,
          essential: false,
          curve: 1.3,
        });
      }, 900);
    });

    return () => map.remove();
  }, [lat, lng]);

  return <div ref={containerRef} className="globe" aria-label="マッチした場所の地球儀表示" />;
}
