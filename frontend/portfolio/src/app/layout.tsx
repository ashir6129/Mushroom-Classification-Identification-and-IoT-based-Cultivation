import type { Metadata } from "next";
import { Outfit, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";

const outfit = Outfit({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Muhammad Ashir Khan | Software Developer",
  description:
    "Portfolio of Muhammad Ashir Khan - Computer Science student at FAST NUCES, Software Developer. I build, I adapt, and I can learn anything.",
  keywords: [
    "Muhammad Ashir Khan",
    "Software Developer",
    "Computer Science",
    "FAST NUCES",
    "Portfolio",
    "Web Developer",
    "Flutter Developer",
  ],
  authors: [{ name: "Muhammad Ashir Khan" }],
  openGraph: {
    title: "Muhammad Ashir Khan | Software Developer",
    description: "I build, I adapt, and I can learn anything.",
    url: "https://ashirkhan.dev",
    siteName: "Muhammad Ashir Khan",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body
        className={`${outfit.variable} ${jetbrainsMono.variable} antialiased bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans`}
      >
        <Navbar />
        <main>{children}</main>
      </body>
    </html>
  );
}
