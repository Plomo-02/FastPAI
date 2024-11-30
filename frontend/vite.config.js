import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";

export default defineConfig({
	server: {
		port: 3000,
		host: true
	},
	plugins: [
		react(),
		svgr({
			include: "**/*.svg?react"
		})
	],
	build: {
		outDir: "./build"
	}
});
