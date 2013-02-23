<Query Kind="Program">
  <Reference>&lt;RuntimeDirectory&gt;\System.Drawing.dll</Reference>
  <Namespace>System.Drawing</Namespace>
  <Namespace>System.Drawing.Imaging</Namespace>
</Query>

void Main()
{
	Merge(new Bitmap(@"C:\dqss\temp\schoolctf\qr\buff-alf1.jpg"), new Bitmap(@"C:\dqss\temp\schoolctf\qr\qrcode_divide.png")).Save(@"C:\dqss\temp\schoolctf\qr\alf.bmp", ImageFormat.Bmp);
}

Bitmap Merge(Bitmap bmp, Bitmap alpha)
{
	Bitmap result = new Bitmap(bmp);
	for (int i = 0; i < Math.Min(bmp.Width, alpha.Width); i++)
	{
		for (int j = 0; j < Math.Min(bmp.Height, alpha.Height); j++)
		{
			Color c = bmp.GetPixel(i, j);
			result.SetPixel(i, j, Color.FromArgb(alpha.GetPixel(i, j).Name == "ff000000" ? 254 : 255, c.R, c.G, c.B));
		}
	}
	return result;
}