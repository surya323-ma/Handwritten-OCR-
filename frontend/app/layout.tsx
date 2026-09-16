import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Handwritten Answer Sheet OCR",
  description: "AI-powered handwritten answer sheet digitization",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="h-screen overflow-hidden">{children}</body>
    </html>
  );
}
