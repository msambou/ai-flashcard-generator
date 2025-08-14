import react from "@vitejs/plugin-react"

// https://vitejs.dev/config/
export default function myDefineConfig() {
  return {
    plugins: [react()],
    server: {
      port: 5173,
      host: true,
    },
  }
}
