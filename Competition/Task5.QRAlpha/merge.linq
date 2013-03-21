<Query Kind="Program">
  <Reference>&lt;RuntimeDirectory&gt;\System.Drawing.dll</Reference>
  <Namespace>System.Drawing</Namespace>
  <Namespace>System.Drawing.Imaging</Namespace>
</Query>

void Main()
{
	ApplyMasks(@"G:\git\ural-schoolctf-2013\competition\task5.qralpha\");
}

void ApplyMasks(string path)
{
	Merge(new Bitmap(path + @"wallpaper.png"), new Bitmap(path + @"mask_r.png"), 0).Save(path + @"wallpaper_1.png", ImageFormat.Png);
	Merge(new Bitmap(path + @"wallpaper_1.png"), new Bitmap(path + @"mask_g.png"), 1).Save(path + @"wallpaper_2.png", ImageFormat.Png);
	Merge(new Bitmap(path + @"wallpaper_2.png"), new Bitmap(path + @"mask_b.png"), 2).Save(path + @"wallpaper_3.png", ImageFormat.Png);
	Merge(new Bitmap(path + @"wallpaper_3.png"), new Bitmap(path + @"mask_a.png"), 3).Save(path + @"wallpaper_4.bmp", ImageFormat.Bmp);
}

Bitmap Merge(Bitmap bmp, Bitmap alpha, int channel)
{
	Bitmap result = new Bitmap(bmp);
	var r = new Random();
	for (int i = 0; i < Math.Min(bmp.Width, alpha.Width); i++)
	{
		for (int j = 0; j < Math.Min(bmp.Height, alpha.Height); j++)
		{
			Color c = bmp.GetPixel(i, j);
			bool mask = alpha.GetPixel(i, j).ToArgb() << 8 == 0;
			Color newColor = c;
			Func<int, int> filter = q => mask ? q & ~3 : q | 3;
			switch(channel)
			{
			case 0:
				newColor = Color.FromArgb(c.A, filter(c.R), c.G, c.B);
				break;
			case 1:
				newColor = Color.FromArgb(c.A, c.R, filter(c.G), c.B);
				break;
			case 2:
				newColor = Color.FromArgb(c.A, c.R, c.G, filter(c.B));
				break;
			case 3:
				newColor = Color.FromArgb(filter(c.A), c.R, c.G, c.B);
				break;
			}
			result.SetPixel(i, j, newColor);
		}
	}
	return result;
}