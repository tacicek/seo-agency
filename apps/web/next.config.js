module.exports = {
	reactStrictMode: true,
	experimental: { appDir: true },
	// Produziere standalone-Output für kompaktere Runtime-Images
	output: 'standalone',
	// Proxy-Rewrite: Leitet Browser-Requests unter /api an den internen FastAPI-Service weiter
	async rewrites() {
		const base = process.env.API_INTERNAL_URL || 'http://api:8000';
		return [
			{
				source: '/api/:path*',
				destination: `${base}/:path*`,
			},
		];
	},
}