import { useState } from 'react';
import { Menu, X, Compass, BookOpenText, Landmark, Github } from 'lucide-react';

const navItems = [
  { href: '#workspace', label: 'Scanner', icon: Compass },
  { href: '#research', label: 'Research', icon: BookOpenText },
  { href: '#policy', label: 'Policy', icon: Landmark },
];

const Navbar = () => {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-2 z-40">
      <nav className="surface mx-auto flex w-full items-center justify-between rounded-2xl px-4 py-2.5 md:px-5">
        <a href="#top" className="inline-flex items-center gap-3" onClick={() => setOpen(false)}>
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-[#dff3f0] text-[#0a4a45]">
            <Compass size={18} />
          </span>
          <span>
            <span className="kicker block">Dark Pattern Lab</span>
            <span className="text-[0.92rem] font-extrabold text-slate-900">Compliance Navigator</span>
          </span>
        </a>

        <div className="hidden items-center gap-2 md:flex">
          {navItems.map(({ href, label, icon: Icon }) => (
            <a
              key={label}
              href={href}
              className="inline-flex items-center gap-2 rounded-full border border-[#ccb68f] bg-[#f8efdf] px-3 py-1.5 text-xs font-bold text-[#5e5139] transition hover:border-[#75ada8] hover:bg-[#dff3f0] hover:text-[#0a4a45]"
            >
              <Icon size={14} />
              {label}
            </a>
          ))}
          <a
            href="https://github.com/shivsingh2005/Darkpattern"
            target="_blank"
            rel="noreferrer"
            className="ml-2 inline-flex items-center gap-2 rounded-full border border-[#75ada8] bg-[#dff3f0] px-3 py-1.5 text-xs font-extrabold uppercase tracking-wide text-[#0a4a45] transition hover:bg-[#cae9e5]"
          >
            <Github size={14} />
            GitHub
          </a>
        </div>

        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          className="grid h-9 w-9 place-items-center rounded-lg border border-[#ccb68f] bg-[#f8efdf] text-[#5e5139] md:hidden"
          aria-label="Toggle navigation menu"
        >
          {open ? <X size={18} /> : <Menu size={18} />}
        </button>
      </nav>

      {open && (
        <div className="surface mt-2 flex flex-col gap-2 rounded-2xl p-3 md:hidden">
          {navItems.map(({ href, label, icon: Icon }) => (
            <a
              key={label}
              href={href}
              onClick={() => setOpen(false)}
              className="inline-flex items-center gap-2 rounded-lg border border-[#ccb68f] bg-[#f8efdf] px-3 py-2 text-sm font-semibold text-[#5e5139]"
            >
              <Icon size={16} />
              {label}
            </a>
          ))}
          <a
            href="https://github.com/shivsingh2005/Darkpattern"
            target="_blank"
            rel="noreferrer"
            onClick={() => setOpen(false)}
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#0f766e] px-3 py-2 text-sm font-bold text-white"
          >
            <Github size={16} />
            Open GitHub
          </a>
        </div>
      )}
    </header>
  );
};

export default Navbar;