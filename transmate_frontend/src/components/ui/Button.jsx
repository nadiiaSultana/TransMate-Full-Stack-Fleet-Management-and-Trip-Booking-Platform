const Button=({children,type='button',onClick,className='',disabled=false})=><button type={type} onClick={onClick} disabled={disabled} className={`rounded-lg bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700 disabled:bg-gray-400 ${className}`}>{children}</button>;
export default Button;
