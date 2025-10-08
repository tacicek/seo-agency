import "../styles/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SEO Analyzer",
  description: "Analyze your website SEO performance",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
