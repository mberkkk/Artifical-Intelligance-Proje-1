using System;
using System.Collections.Generic;
using System.Linq;

public class GeneticAlgorithm
{
	// Bir populasyonda  bulunan kromozom sayısı
	private const int POPULATION_SIZE = 100;

	// Kullanılabilir genler 
	private const string GENES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP" +
								"QRSTUVWXYZ 1234567890, .-;:_!\"#%&/()=?@${[]}";

	// Bulunup kırılmak için şifre belirtilir
	private const string KEY = "(Generative AI) ";

	// Mutasyon, Çaprazlama vb. fonksiyonlarda kullanmak üzere Random bileşeni eklenilir
	private static readonly Random random = new Random();

	// Başlangıç ve bitiş sayıları verilmiş olan ardışık sayıların içerisinden rastgele bir integer döndürecek fonksiyon. Rastgele index elde etmek için kullanılır. 
	private static int RandomNum(int start, int end)
	{
		return random.Next(start, end + 1);
	}

	// Gen dizisi; aranan şifreye daha yakın olan, yani daha çok umut vaad eden kromozomlara çaprazlama işleminde daha çok rastlanabilmesi için kullanılan bir fonksiyondur.
	// Amaç daha iyi olan kromozomlar üzerinden ilerleyerek sonuca yaklaşmaktır
	private static int genomeRoulette(int start, int end)
	{
		double p = random.NextDouble();

		//Jenerasyon Fitness değerlerine göre sıralandığı için istenen sonuca daha yakın olan kromozomlar ilk kısımlarda yer alacaktır

		if (p < 0.5)
		{
			return random.Next(start, (start + end) / 2);

		}
		else if (p < 0.8)
		{
			return random.Next(start, end + 1);
		}
		else
		{
			return random.Next((start + end) / 2, end + 1);
		}
	}

	// Kromozomları fitness değerlerine göre sıralayan fonksiyon
	private class FitnessComparer : IComparer<Cromosome>
	{
		public int Compare(Cromosome ind1, Cromosome ind2)
		{
			return ind1.FitnessValue.CompareTo(ind2.FitnessValue);
		}
	}

	// Mutation fonksiyonu ile rastgele bir şekilde genom oluşturan fonksiyon 
	private static string CreateCromosome()
	{
		int len = KEY.Length;
		char[] genome = new char[len];
		for (int i = 0; i < len; i++)
		{
			genome[i] = Mutation();
		}
		return new string(genome);
	}

	// Rastgele bir şekilde gen değiştirmemizi yarayan fonksiyon
	private static char Mutation()
	{
		int len = GENES.Length;
		int r = RandomNum(0, len - 1);
		return GENES[r];
	}

	//Genetik Algoritmanın temel yapı taşı olan kromozom sınıfı
	private class Cromosome
	{
		// Her kromozomun bir içeriği yani genomu vardır
		public string dna { get; }
		// Her kromozomun istenen sonuca ne kadar yakın olduğunu gösteren bir uygunluk değeri (Fitness Value) vardır
		public int FitnessValue { get; }

		//Generator fonksiyon
		public Cromosome(string chromosome)
		{
			dna = chromosome;
			FitnessValue = CalculateFitness();
		}

		// Fitness değerini hesaplayan fonksiyon
		private int CalculateFitness()
		{
			// Kod parçası, dna ve KEY koleksiyonlarını karşılaştırarak eşleşmeyen her çift için 1, eşleşen çiftler için ise 0 döndürerek kromozomun fitness değerini hesaplar.
			return dna.Zip(KEY, (a, b) => a == b ? 0 : 1).Sum();
		}

		// Çaprazlama ile yeni jenerasyona ait bir kromozom oluşturma işlemi gerçekleştirilir
		public Cromosome Cross(Cromosome parent2)
		{
			// Yeni jenerasyona ait yeni bir kromozom oluşturulur
			char[] childChromosome = new char[dna.Length];

			//Çaprazlama işlemi gerçekleştirilir
			for (int i = 0; i < dna.Length; i++)
			{
				double p = random.NextDouble();
				if (p < 0.45)
					childChromosome[i] = dna[i];
				else if (p < 0.90)
					childChromosome[i] = parent2.dna[i];
				else
					childChromosome[i] = Mutation();//Düşük bir olasılıkla da olsa childChromosome geni parentlarından değil, mutasyon ile rastgele bir şekilde alır
			}
			return new Cromosome(new string(childChromosome));
		}
	}

	public static void Main()
	{
		//Algoritmanın ne kadar sürede gerçekleşeceiğini belirlemek için kronometre çalıştırılır.
		var watch = System.Diagnostics.Stopwatch.StartNew();

		// Şifrenin kaçıncı jenerasyonda kırıldığını takip etmek için kullanılan bir sayaç
		int generation = 0;	

		List<Cromosome> population = new List<Cromosome>();
		//Genetik algoritmanın hangi aşamada sonlanacağını belirlemek için kullanılan bool değer
		bool didKeyBroke = false;

		//ilk populasyon oluşturulur
		for (int i = 0; i < POPULATION_SIZE; i++)
		{
			string genome = CreateCromosome();
			population.Add(new Cromosome(genome));
		}

		while (!didKeyBroke)
		{
			// populasyon fitnes değerlerine göre artan sırada sıralanır
			population.Sort(new FitnessComparer());

			//Fitness değeri ne kadar küçükse şifreye o kadar yaklaşılmış demektir
			//Eğerki populasyonun ilk kromozomu (yani populasyonun sonuca en yakın kromozomu) fitness değeri 0 ise şifre kırılmış demektir.Algoritma sonlanır
			if (population[0].FitnessValue == 0)
			{
				didKeyBroke = true;
				break;
			}

			// Eğer algoritma sonlanmadıysa bir sonraki jenerasyon oluşturulmaya başlanır
			List<Cromosome> newGeneration = new List<Cromosome>();

			// Bir önceki jenerasyonun ilk %10'luk kısmı yani jenerasyonun en iyileri bir sonraki jenerasyona aktarılır. Buna Elitizm denir
			// Amaç umut verici olan kromozomlar üzerinden ilerlemeye devam edilerek sonuca ulaşmaktır
			int s = (10 * POPULATION_SIZE) / 100;
			for (int i = 0; i < s; i++)
				newGeneration.Add(population[i]);

			// Populasyonun %10'u Elitizm ile belirlendiği için geri kalan %90'lık kısım çaprazlama ile belirlenir
			s = (90 * POPULATION_SIZE) / 100;
			for (int i = 0; i < s; i++)
			{
				int len = population.Count;
				int r = genomeRoulette(0, 50);//Genom Çarkı ile çaprazlamda kullanılacak olan parentlar belirlenir.Sonuca daha yakın olan kromozomların çaprazlanmada kullanılma olasılığı daha yüksektir
				Cromosome parent1 = population[r];
				r = genomeRoulette(0, 50);
				Cromosome parent2 = population[r];
				Cromosome newCromosome = parent1.Cross(parent2);
				newGeneration.Add(newCromosome);//Yeni kromozom oluşturulur
			}
			//Yeni jenerasyon, asıl jenerasyonun yerini alarak sonraki işlemlerin kendisi üzerinden devam edilmesini sağlar
			population = newGeneration;
			//Kaçıncı jenerasyonda DNA'nın hangi durumda olduğu ve sonuca ne kadar yakın olduğu yazdırılarak algoritmanın takibi sağlanır
			Console.WriteLine("Generation: " + generation + "\t" +
							"String: " + population[0].dna + "\t" +
							"Fitness: " + population[0].FitnessValue);

			generation++;
		}

		//Kronometre sonlandırılarak işlemin gerçekleşme süresi hesaplanır
		watch.Stop();

		Console.WriteLine("Generation: " + generation + "\t" +
						"String: " + population[0].dna + "\t" +
						"Fitness: " + population[0].FitnessValue + "\t" +
						"Execution Time: " + watch.ElapsedMilliseconds + " Milisecond");
	}
}
