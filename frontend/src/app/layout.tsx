import "./globals.css";
import Header from "@/components/Header"; 

export const metadata = {
  title: "Todo App",
  description: "Modern Task Management",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-100">
        <Header /> 
        <main>{children}</main>
      </body>
    </html>
  );
}