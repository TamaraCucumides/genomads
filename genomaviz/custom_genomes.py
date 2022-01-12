import warnings
import genomaviz.colors

class Polinomio():
    
    def __init__(self, cog={}, pol={}):
        self.capacities_thresh_cog = cog
        self.capacities_thresh_pol = pol
        
        total_weight=0
        for key in {**self.capacities_thresh_cog, **self.capacities_thresh_pol}.keys():
            total_weight += {**self.capacities_thresh_cog, **self.capacities_thresh_pol}[key]["weight"]
        if int(total_weight*100) != 100:
            warnings.warn(
                "Variable weights add up to {}%".format(int(total_weight*100)),
                UserWarning)


    def calculate_score(self, query_params, score_modifier=None):
        score_cap = 0
        for t_id in list(self.capacities_thresh_cog.keys()):
            level = self.capacities_thresh_cog[t_id]["level"]
            weight = self.capacities_thresh_cog[t_id]["weight"]
            user_trait = int(query_params.get(t_id))
            user_score  = min(1, user_trait/level) * weight * 100
            score_cap += user_score
        for t_id in list(self.capacities_thresh_pol.keys()):
            level_to = self.capacities_thresh_pol[t_id]["level_to"]
            level_from = self.capacities_thresh_pol[t_id]["level_from"]
            weight = self.capacities_thresh_pol[t_id]["weight"]
            user_trait = int(query_params.get(t_id))

            if user_trait < level_from:
                user_score = (100 - abs(user_trait - level_from)) * weight
            elif user_trait > level_to:
                user_score = (100 - abs(user_trait - level_to)) * weight
            else:
                user_score = 100 * weight

            score_cap += user_score
        
        if score_modifier is None:
            return int(score_cap)
        else:
            return score_modifier(score_cap)
    

    def predict(self, data, out_var, print_results=False):
        self.edd = []
        self.fit = []
        if print_results:
            print("{0: >8} | {1: >8}".format("Real", "Fit Pred"))
        for i in range(data.shape[0]):

            if print_results:
                print("{0: >8} | {1: >8}".format(int(data.iloc[i][out_var]), self.calculate_score(data.iloc[i])))
            self.edd.append(int(data.iloc[i][out_var]))
            self.fit.append(self.calculate_score(data.iloc[i]))
        

    def prediction_plot(self, palette=saturated_palette, xlines=[0.5,1.5], ylines=[60,85]):
        sns.scatterplot(x=self.edd, y=self.fit, color=palette[0])
        if (len(xlines) > 3) or (len(ylines) > 3):
            raise ValueError("Can't plot more than 3 lines per axis")
        xline_palette = ["r", "y", "g"]
        xline_palette = xline_palette[len(xline_palette)-len(xlines):]
        yline_palette = ["r", "y", "g"]
        yline_palette = yline_palette[len(yline_palette)-len(ylines):]
        
        for i, xline in reversed(list(enumerate(xlines))):
            plt.axvline(x = xline, color = xline_palette[i], linestyle = ':')
            
        for j, yline in reversed(list(enumerate(ylines))):
            plt.axhline(y = yline, color = yline_palette[j], linestyle = ':')

        plt.xlim([xlines[0]-1, xlines[1]+1])
        plt.ylim([-5, 105])
        plt.ylabel("Fit predicho")
