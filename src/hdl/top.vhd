library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
-- use IEEE.NUMERIC_STD.ALL;

entity top is
    Port (
        clk : in  STD_LOGIC;                       -- 100 MHz (W5)
        sw  : in  STD_LOGIC_VECTOR(15 downto 0);   -- Interruptores SW0-SW15
        btn : in  STD_LOGIC_VECTOR(4 downto 0);    -- Botones: C U L R D
        led : out STD_LOGIC_VECTOR(15 downto 0);   -- LEDs LD0-LD15
        seg : out STD_LOGIC_VECTOR(6 downto 0);    -- Segmentos CA-CG (activo bajo)
        dp  : out STD_LOGIC;                       -- Punto decimal (activo bajo)
        an  : out STD_LOGIC_VECTOR(3 downto 0)    -- Ánodos del display (activo bajo)
    );
end top;

architecture Behavioral of top is
begin

    -- TODO: Implementa tu diseño aquí
    led <= sw;

    -- Display apagado
    seg <= (others => '1');
    dp  <= '1';
    an  <= (others => '1');

end Behavioral;
