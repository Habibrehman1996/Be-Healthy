import './globals.css';

export const metadata = { title: 'Be Healthy' };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}